import os

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.resources.generators.linear_equations_lesson import build_lesson

FILENAME = "Algebra-OneStepVar1Side-NonCalc.pptx"


class Command(BaseCommand):
    help = (
        "Generates the 'Белгисиз бир жагында: 1-кадам' (one-step equations) "
        "teaching presentation into media/resources/files/, where "
        "import_resources picks it up by filename."
    )

    def handle(self, *args, **options):
        out_dir = os.path.join(settings.MEDIA_ROOT, "resources", "files")
        os.makedirs(out_dir, exist_ok=True)

        out_path = os.path.join(out_dir, FILENAME)
        build_lesson().save(out_path)
        self.stdout.write(self.style.SUCCESS(f"Written {out_path}"))
