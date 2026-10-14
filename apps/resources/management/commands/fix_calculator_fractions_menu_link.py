from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem

# "Калькулятордо бөлчөктөр" (under Сандар > Калькулятор колдонуу) used to
# resolve to the old generic Topic/Subtopic/SubSubtopic page
# (subsubtopic_detail + topic_page.html), which has zero Resource content.
# It now has a dedicated page built on the same topic_materials.html
# template as to-fractions (see apps/resources/views/calculator.py), so
# this clears the subtopic/subsubtopic FKs (get_resolved_url() would
# otherwise win over url_name) and points the menu link at it directly -
# the same pattern the 'to_fractions' MenuItem already uses. Idempotent.


class Command(BaseCommand):
    help = (
        "Repoints the 'Калькулятордо бөлчөктөр' menu item at the new "
        "calculator_fractions_view instead of the empty generic "
        "Topic/SubSubtopic page. Idempotent - safe to re-run."
    )

    def handle(self, *args, **options):
        updated = MenuItem.objects.filter(title='Калькулятордо бөлчөктөр').update(
            topic=None, subtopic=None, subsubtopic=None, url_name='calculator_fractions',
        )
        if updated:
            self.stdout.write(self.style.SUCCESS(
                f"Repointed {updated} 'Калькулятордо бөлчөктөр' menu item(s) to calculator_fractions."
            ))
        else:
            self.stdout.write(self.style.WARNING("No 'Калькулятордо бөлчөктөр' menu item found."))
