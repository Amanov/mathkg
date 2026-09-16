import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from ...models import Resource

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        folder = os.path.join(settings.MEDIA_ROOT, 'resources', 'files')

        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)

            # ADD THIS LINE — skip subfolders
            if os.path.isdir(filepath):
                self.stdout.write(f'Skipping folder: {filename}')
                continue

            if Resource.objects.filter(title=filename).exists():
                self.stdout.write(f'Skipping {filename} — already exists')
                continue

            # guess category from filename
            if filename.endswith('.pptx'):
                category = 'presentation'
            elif filename.endswith('.pdf'):
                category = 'worksheet'
            else:
                category = 'activity'

            with open(filepath, 'rb') as f:
                resource = Resource(
                    title=filename,
                    category=category,
                    is_active=True,
                )
                resource.file.save(filename, File(f), save=True)
                self.stdout.write(f'Imported: {filename}')

        self.stdout.write('Done!')