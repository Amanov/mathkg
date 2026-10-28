"""Copy git-tracked resource files that the media volume does not have yet.

Revisions that still track ``media/`` can fill a volume that is missing
a file. After ``media/`` is gitignored, this command finds nothing new
there. New files ship from ``apps/resources/bundled_files/``.

On Railway, /app/media is a mounted volume, so files added under
media/resources/files/ in git are hidden from the running app. This
command reads those paths from git and writes any file that is not
already on MEDIA_ROOT. A file that is already there is left untouched.
"""

import os
import subprocess
import tarfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

TRACKED_PREFIX = 'media/resources/files/'


class Command(BaseCommand):
    help = (
        'Copy git-tracked media/resources/files onto MEDIA_ROOT when the '
        'file is missing there. Never overwrites an existing file.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            help=(
                'Git checkout to read from. Use this on Railway after '
                'cloning the deployed revision somewhere outside /app/media. '
                'Defaults to this app checkout.'
            ),
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print the files that would be copied, and write nothing.',
        )

    def handle(self, *args, **options):
        repo = _repo_root(options['source'] or settings.BASE_DIR)
        dest_root = Path(settings.MEDIA_ROOT) / 'resources' / 'files'
        dest_root.mkdir(parents=True, exist_ok=True)

        copied = skipped = 0
        for rel, data in _tracked_files(repo):
            dest = _destination(dest_root, rel)
            if dest is None:
                self.stderr.write(f'Skipping unsafe path: {rel}')
                continue
            if dest.is_symlink() or dest.exists():
                skipped += 1
                continue
            copied += 1
            self.stdout.write(str(Path(TRACKED_PREFIX) / rel))
            if options['dry_run']:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                fd = os.open(dest, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                copied -= 1
                skipped += 1
                continue
            with os.fdopen(fd, 'wb') as out:
                out.write(data)

        verb = 'Would copy' if options['dry_run'] else 'Copied'
        self.stdout.write(f'{verb} {copied} file(s). Left {skipped} existing file(s) unchanged.')


def _repo_root(start):
    start = Path(start)
    if not start.exists():
        raise CommandError(f'Source does not exist: {start}')
    proc = subprocess.run(
        ['git', '-C', str(start), 'rev-parse', '--show-toplevel'],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or '').strip()
        raise CommandError(
            'Could not read git-tracked resource files'
            + (f' ({detail})' if detail else '')
            + '.\n'
            'On Railway the /app/media volume hides the copy baked into the '
            'image. From a shell, with the app virtualenv active:\n'
            '  git clone --depth 1 https://github.com/Amanov/mathkg.git '
            '/tmp/mathkg-media\n'
            '  python manage.py copy_missing_resource_files '
            '--source /tmp/mathkg-media'
        )
    return Path(proc.stdout.strip())


def _tracked_files(repo):
    """Yield (path under resources/files, bytes) from git, one file at a time.

    git archive reads blobs, so a volume mounted over the working tree's
    media directory does not hide them.
    """
    proc = subprocess.Popen(
        ['git', '-C', str(repo), 'archive', '--format=tar', 'HEAD', TRACKED_PREFIX],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        with tarfile.open(fileobj=proc.stdout, mode='r|') as archive:
            for member in archive:
                extracted = archive.extractfile(member) if member.isfile() else None
                data = extracted.read() if extracted is not None else b''
                if not member.isfile():
                    continue
                name = member.name.replace('\\', '/')
                if not name.startswith(TRACKED_PREFIX):
                    continue
                yield name[len(TRACKED_PREFIX):], data
    finally:
        if proc.stdout:
            proc.stdout.close()
        err = proc.stderr.read() if proc.stderr else b''
        code = proc.wait()
    if code != 0:
        detail = err.decode(errors='replace').strip()
        raise CommandError(detail or f'git archive failed ({code})')


def _destination(dest_root, rel):
    parts = Path(rel).parts
    if not parts or any(part in ('', '.', '..') for part in parts):
        return None
    dest = dest_root.joinpath(*parts)
    if dest_root not in dest.parents:
        return None
    return dest
