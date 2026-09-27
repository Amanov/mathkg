import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.resources.models import Resource

TEMPLATES_DIR = os.path.join('templates', 'resources', 'ekvivalenttuuluk')
FILENAME_RE = re.compile(r"res\|get_item:'([^']+)'")


class Command(BaseCommand):
    help = (
        "Creates the Resource rows the 9 Ондуктар > Эквиваленттүүлүк pages "
        "need (see apps/resources/views/ekvivalenttuuluk.py). Their backing "
        "files already sit in media/resources/files/ (git-tracked, same as "
        "every other resource) - this only creates the missing Resource DB "
        "rows, pointing the FileField straight at the existing file path "
        "rather than re-uploading it (re-uploading would treat the already-"
        "present file as a name collision and write a second, renamed copy "
        "alongside it). Idempotent - skips any filename that already has a "
        "Resource, safe to re-run."
    )

    def handle(self, *args, **options):
        templates_root = os.path.join(settings.BASE_DIR, TEMPLATES_DIR)
        filenames = set()
        for fname in os.listdir(templates_root):
            with open(os.path.join(templates_root, fname), encoding='utf-8') as fh:
                filenames.update(FILENAME_RE.findall(fh.read()))

        created = skipped_missing = already_exist = 0
        for filename in sorted(filenames):
            if Resource.objects.filter(title=filename).exists():
                already_exist += 1
                continue

            rel_path = f'resources/files/{filename}'
            abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            if not os.path.exists(abs_path):
                self.stderr.write(f'  MISSING on disk, skipped: {filename}')
                skipped_missing += 1
                continue

            ext = filename.rsplit('.', 1)[-1].lower()
            category = 'presentation' if ext == 'pptx' else 'worksheet'
            resource = Resource(title=filename, category=category, is_active=True)
            resource.file.name = rel_path
            resource.save()
            created += 1
            self.stdout.write(f'  Created: {filename}')

        self.stdout.write(self.style.SUCCESS(
            f'Created {created}, already existed {already_exist}, missing {skipped_missing}.'
        ))
