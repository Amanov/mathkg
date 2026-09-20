from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, Resource, SubSubtopic, Subtopic, Topic

from apps.resources.data.four_basic_operations_data import FOUR_BASIC_OPERATIONS_SECTIONS
from apps.resources.data.directed_numbers_data import DIRECTED_NUMBERS_SECTIONS
from apps.resources.data.all_operations_data import ALL_OPERATIONS_SECTIONS
from apps.resources.data.koshuu_1_digit_data import KOSHUU_1_DIGIT_SECTIONS

TOPIC_TITLE = 'Сандар'
TOPIC_SLUG = 'number'

# Mirrors the branches expand_number_menu.py already added under 'Сандар' -
# this command doesn't create menu items, only repoints the leaves that
# command already created at the new generic subsubtopic pages.
SUBTOPICS = {
    'Бүтүн сандар менен амалдар': {
        'slug': 'whole-number-operations',
        'order': 3,
        'subsubtopics': {
            'Багытталган сандар': {'slug': 'directed-numbers', 'order': 1, 'sections': DIRECTED_NUMBERS_SECTIONS},
            'Төрт амал': {'slug': 'four-basic-operations', 'order': 2, 'sections': FOUR_BASIC_OPERATIONS_SECTIONS},
            'Аралаш амалдар': {'slug': 'mixed-operations', 'order': 3, 'sections': ALL_OPERATIONS_SECTIONS},
        },
    },
    'Ондуктар менен эсептөө': {
        'slug': 'decimal-computation',
        'order': 4,
        'subsubtopics': {
            'Кошуу (1 орундук сандар)': {'slug': 'koshuu-1-digit', 'order': 1, 'sections': KOSHUU_1_DIGIT_SECTIONS},
        },
    },
}


def guess_learning_goal(header):
    text = header.lower()
    if 'киришүү' in text or 'презентац' in text:
        return 'presentation'
    if 'тактада' in text or 'көрсөтмө' in text or 'think' in text or 'reason' in text:
        return 'discussion'
    if 'иш барактар' in text or 'practice' in text or 'fluency' in text:
        return 'fluency'
    if 'учурундагы' in text or 'conceptual' in text:
        return 'discovery'
    if 'оюндар' in text or 'көндүмдөр' in text:
        return 'games'
    if 'challenge' in text:
        return 'problem_solving'
    if 'reflect' in text or 'assess' in text:
        return 'retrieval'
    if 'teacher' in text or 'parent' in text:
        return 'modelling'
    return 'fluency'


class Command(BaseCommand):
    help = (
        "Links the existing Resource rows behind the 4 bespoke Сандар pages "
        "(four_basic_operations, directed_numbers, all_operations, "
        "koshuu_1_digit) into the generic Topic/Subtopic/SubSubtopic system, "
        "by matching Resource.title against the filenames already listed in "
        "each page's data file - it never creates Resource rows, only links "
        "ones that already exist; an unmatched filename is reported and "
        "skipped safely. Creates 2 Subtopics ('Бүтүн сандар менен амалдар', "
        "'Ондуктар менен эсептөө') and their Sub-subtopics under the "
        "existing 'Сандар' topic, and repoints the matching MenuItem leaves "
        "(added earlier by expand_number_menu) at the new generic "
        "subsubtopic pages. The old bespoke routes/views/templates are left "
        "completely untouched and keep working. Idempotent - safe to "
        "re-run. Pass --undo to remove the 2 Subtopics (Resource "
        "subtopic/subsubtopic FKs auto-reset to NULL via on_delete=SET_NULL) "
        "and clear the MenuItem FKs, reverting the leaves to their original "
        "url_name-based links; Resource.topic/learning_goal set along the "
        "way are left as-is since they remain accurate either way."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--undo', action='store_true',
            help="Unlink everything this command added, instead of adding it.",
        )

    def handle(self, *args, **options):
        if options['undo']:
            self.undo()
        else:
            self.apply()

    def apply(self):
        topic, created = Topic.objects.get_or_create(
            title=TOPIC_TITLE, defaults={'slug': TOPIC_SLUG}
        )
        verb = 'Created' if created else 'Already exists'
        self.stdout.write(f"{verb} Topic: {topic.title}")

        linked = 0
        missing = []

        for subtopic_title, subtopic_cfg in SUBTOPICS.items():

            subtopic, created = Subtopic.objects.get_or_create(
                title=subtopic_title, topic=topic,
                defaults={'slug': subtopic_cfg['slug'], 'order': subtopic_cfg['order']},
            )
            verb = 'Created' if created else 'Already exists'
            self.stdout.write(f"{verb} Subtopic: {topic.title} > {subtopic.title}")

            menu_parent = MenuItem.objects.filter(
                title=subtopic_title, parent__title=TOPIC_TITLE, parent__parent__isnull=True,
            ).first()
            if menu_parent is None:
                self.stdout.write(self.style.WARNING(
                    f"  No 'Сандар > {subtopic_title}' menu branch found (run expand_number_menu "
                    f"first) - Resources will still be linked, but the menu link won't be repointed."
                ))

            for ss_title, ss_cfg in subtopic_cfg['subsubtopics'].items():

                subsubtopic, created = SubSubtopic.objects.get_or_create(
                    title=ss_title, subtopic=subtopic,
                    defaults={'slug': ss_cfg['slug'], 'order': ss_cfg['order']},
                )
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f"  {verb} Sub-subtopic: {subtopic.title} > {subsubtopic.title}")

                for section in ss_cfg['sections']:
                    goal = guess_learning_goal(section['header'])
                    for block in section['blocks']:
                        for filename in block['files']:
                            resource = Resource.objects.filter(title=filename).first()
                            if resource is None:
                                missing.append(filename)
                                continue

                            changed = []
                            if resource.topic_id != topic.id:
                                resource.topic = topic
                                changed.append('topic')
                            if resource.subtopic_id != subtopic.id:
                                resource.subtopic = subtopic
                                changed.append('subtopic')
                            if resource.subsubtopic_id != subsubtopic.id:
                                resource.subsubtopic = subsubtopic
                                changed.append('subsubtopic')
                            if not resource.learning_goal:
                                resource.learning_goal = goal
                                changed.append('learning_goal')
                            if changed:
                                resource.save(update_fields=changed)
                            linked += 1

                if menu_parent is not None:
                    leaf = MenuItem.objects.filter(title=ss_title, parent=menu_parent).first()
                    if leaf is not None:
                        leaf.topic = topic
                        leaf.subtopic = subtopic
                        leaf.subsubtopic = subsubtopic
                        leaf.save(update_fields=['topic', 'subtopic', 'subsubtopic'])
                        self.stdout.write(f"  Rewired menu link: {menu_parent.title} > {leaf.title}")

        self.stdout.write(self.style.SUCCESS(f"Linked {linked} existing Resource row(s)."))

        if missing:
            self.stdout.write(self.style.WARNING(
                f"{len(missing)} filename(s) referenced in the data files have no matching "
                f"Resource row (by title) - nothing was created for them, check the title spelling "
                f"or whether the file has actually been uploaded via admin yet:"
            ))
            for name in missing:
                self.stdout.write(f"  - {name}")

    def undo(self):
        for subtopic_title, subtopic_cfg in SUBTOPICS.items():

            menu_parent = MenuItem.objects.filter(
                title=subtopic_title, parent__title=TOPIC_TITLE, parent__parent__isnull=True,
            ).first()
            if menu_parent is not None:
                for ss_title in subtopic_cfg['subsubtopics']:
                    MenuItem.objects.filter(title=ss_title, parent=menu_parent).update(
                        topic=None, subtopic=None, subsubtopic=None,
                    )

            deleted, _ = Subtopic.objects.filter(
                title=subtopic_title, topic__title=TOPIC_TITLE,
            ).delete()
            if deleted:
                self.stdout.write(f"Removed Subtopic (and its Sub-subtopics): {subtopic_title}")
            else:
                self.stdout.write(f"Not found (already removed?): {subtopic_title}")

        self.stdout.write(self.style.SUCCESS(
            'Undo complete. Menu leaves reverted to their url_name-based links. Resource rows '
            'were left untouched (subtopic/subsubtopic auto-reset to NULL via on_delete=SET_NULL).'
        ))
