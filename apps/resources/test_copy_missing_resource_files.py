import os
import shutil
import subprocess
import tempfile
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings


def _git(repo, *args):
    subprocess.run(
        ['git', '-C', str(repo), '-c', 'user.email=test@example.com', '-c', 'user.name=Test', *args],
        check=True, capture_output=True,
    )


class CopyMissingResourceFilesTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.repo = os.path.join(self.tmp, 'repo')
        self.media = os.path.join(self.tmp, 'media')
        files = os.path.join(self.repo, 'media', 'resources', 'files')
        os.makedirs(os.path.join(files, 'nested'))
        with open(os.path.join(files, 'new.pptx'), 'wb') as fh:
            fh.write(b'new-bytes')
        with open(os.path.join(files, 'keep.pptx'), 'wb') as fh:
            fh.write(b'from-git')
        with open(os.path.join(files, 'nested', 'inner.pptx'), 'wb') as fh:
            fh.write(b'inner')
        _git(self.repo, 'init')
        _git(self.repo, 'add', 'media')
        _git(self.repo, 'commit', '-m', 'files')
        with open(os.path.join(files, 'untracked.pptx'), 'wb') as fh:
            fh.write(b'not-tracked')

        os.makedirs(os.path.join(self.media, 'resources', 'files'))
        kept = os.path.join(self.media, 'resources', 'files', 'keep.pptx')
        with open(kept, 'wb') as fh:
            fh.write(b'already-on-volume')

    def _run(self, *args):
        out = StringIO()
        call_command(
            'copy_missing_resource_files',
            '--source', self.repo,
            *args,
            stdout=out,
        )
        return out.getvalue()

    def test_copies_missing_tracked_files_and_leaves_existing_bytes_alone(self):
        with override_settings(MEDIA_ROOT=self.media):
            text = self._run()
        dest = os.path.join(self.media, 'resources', 'files')
        with open(os.path.join(dest, 'new.pptx'), 'rb') as fh:
            self.assertEqual(fh.read(), b'new-bytes')
        with open(os.path.join(dest, 'keep.pptx'), 'rb') as fh:
            self.assertEqual(fh.read(), b'already-on-volume')
        with open(os.path.join(dest, 'nested', 'inner.pptx'), 'rb') as fh:
            self.assertEqual(fh.read(), b'inner')
        self.assertFalse(os.path.exists(os.path.join(dest, 'untracked.pptx')))
        self.assertIn('Copied 2 file(s). Left 1 existing file(s) unchanged.', text)
        self.assertIn('new.pptx', text)
        self.assertNotIn('untracked.pptx', text)

        with override_settings(MEDIA_ROOT=self.media):
            again = self._run()
        self.assertIn('Copied 0 file(s). Left 3 existing file(s) unchanged.', again)

    def test_dry_run_writes_nothing(self):
        with override_settings(MEDIA_ROOT=self.media):
            text = self._run('--dry-run')
        dest = os.path.join(self.media, 'resources', 'files')
        self.assertFalse(os.path.exists(os.path.join(dest, 'new.pptx')))
        self.assertIn('Would copy 2 file(s).', text)
        with open(os.path.join(dest, 'keep.pptx'), 'rb') as fh:
            self.assertEqual(fh.read(), b'already-on-volume')

    def test_a_directory_without_git_is_refused(self):
        empty = os.path.join(self.tmp, 'empty')
        os.makedirs(empty)
        with override_settings(MEDIA_ROOT=self.media):
            with self.assertRaises(CommandError):
                call_command('copy_missing_resource_files', '--source', empty)
