from django.core.management.base import BaseCommand

from apps.resources.models import MenuItem, Topic, Subtopic, SubSubtopic

# Translated from a reference UK-curriculum topic tree. Only the topic /
# subtopic / sub-subtopic NAMES are used here - these are standard,
# industry-wide curriculum terms (BIDMAS, Decimals, Ratio, ...), not
# anyone's proprietary content. The individual worksheet-level titles from
# that tree are deliberately NOT imported: Resource requires a real
# uploaded file, so turning ~250 of them into DB rows would only produce
# dead "no file" entries - real worksheets get added through the admin
# (see apps/resources/models.py Resource) once they exist, and will show
# up under whichever of these sub-subtopics they belong to.
#
# Structure per topic: {subtopic_title: {'slug': ..., 'subsubtopics': {...}}}
# subsubtopics is {} for a subtopic whose reference entry was a plain list
# (no third level) - it still gets its own browsable page, just with no
# further nesting in the menu.

TAXONOMY = {
    'Сандар': {
        'slug': 'number',
        'menu_order_start': 100,  # existing manual children use order 1-4
        'subtopics': {
            'Амалдардын тартиби': {'slug': 'bidmas', 'subsubtopics': {}},
            'Ондуктар': {
                'slug': 'decimals',
                'subsubtopics': {
                    'Эсептөөлөр: 1 орундук сандар': 'arithmetic-1-digit',
                    'Эсептөөлөр: 1 жана 2 орундук сандар': 'arithmetic-1-2-digit',
                    'Эсептөөлөр: бүтүн сандар менен': 'arithmetic-with-integers',
                    'Эквиваленттүүлүк': 'equivalence',
                    'Акча': 'money',
                    'Мезгилдүү ондуктар': 'recurring',
                    'Башка': 'other',
                },
            },
            'Багытталган сандар': {
                'slug': 'directed-numbers',
                'subsubtopics': {
                    'Эсептөөлөр': 'arithmetic',
                },
            },
            'Эквиваленттүүлүк': {
                'slug': 'equivalence',
                'subsubtopics': {
                    'Бөлчөктөрдү айландыруу': 'converting-fractions',
                    'Ондуктарды айландыруу': 'converting-decimals',
                    'Пайыздарды айландыруу': 'converting-percentages',
                    'Катыштарды айландыруу': 'converting-ratios',
                },
            },
            'Болжолдоо жана тегеректөө': {
                'slug': 'estimating-rounding',
                'subsubtopics': {
                    'Болжолдоо': 'estimating',
                    'Тегеректөө': 'rounding',
                    'Ката аралыктары': 'error-intervals',
                },
            },
            'Бөлүүчүлөр, эселиктер жана жөнөкөй сандар': {
                'slug': 'factors-multiples-primes',
                'subsubtopics': {
                    'Негиздери': 'basics',
                    'Эң чоң орток бөлүүчү жана эң кичине орток эселик: тизмелөө менен': 'hcf-lcm-listing',
                    'Эң чоң орток бөлүүчү жана эң кичине орток эселик: жөнөкөй көбөйтүүчүлөргө ажыратуу менен': 'hcf-lcm-prime-factorisation',
                },
            },
            'Бөлчөктөр': {
                'slug': 'fractions',
                'subsubtopics': {
                    'Киришүү': 'introduction',
                    'Эсептөөлөр: бирдик бөлчөктөр': 'arithmetic-unit-fractions',
                    'Эсептөөлөр: бирдик эмес бөлчөктөр': 'arithmetic-non-unit-fractions',
                    'Барабар бөлчөктөр': 'equivalent-fractions',
                    'Туюнтуу': 'expressing',
                    'Чоңдуктун бөлчөгү': 'fraction-of-a-quantity',
                    'Аралаш сандар жана туура эмес бөлчөктөр': 'mixed-numbers-improper-fractions',
                },
            },
            'Даражалар жана тамырлар': {
                'slug': 'indices-surds',
                'subsubtopics': {
                    'Даражалар': 'indices',
                    'Тамырларды эсептөө': 'evaluating-roots',
                    'Тамырлар менен эсептөөлөр': 'surds',
                },
            },
            'Бүтүн сандар': {
                'slug': 'integers',
                'subsubtopics': {
                    'Негиздери': 'basics',
                    'Эсептөөлөр: 1 жана 2 орундук': 'arithmetic-1-2-digit',
                    'Эсептөөлөр: 2 жана 3 орундук': 'arithmetic-2-3-digit',
                    'Турмуштук маселелер': 'real-life',
                },
            },
            'Өлчөмдөр': {
                'slug': 'measures',
                'subsubtopics': {
                    'Татаал өлчөмдөр': 'compound',
                    'Масштабдуу сүрөттөр': 'scale-drawings',
                    'Өлчөө системалары': 'systems-of-measurement',
                    'Убакыт': 'time',
                },
            },
            'Стандарттык форма': {
                'slug': 'standard-form',
                'subsubtopics': {
                    'Негиздери': 'basics',
                    'Көбөйтүү жана бөлүү': 'multiplying-dividing',
                    'Айландыруу': 'converting',
                },
            },
            'Системалуу тизмелөө': {'slug': 'systematic-listing', 'subsubtopics': {}},
            'Эсептөөнүн көбөйтүү эрежеси': {'slug': 'product-rule-for-counting', 'subsubtopics': {}},
            'Калькулятор колдонуу': {'slug': 'using-a-calculator', 'subsubtopics': {}},
        },
    },
    'Пропорция': {
        'slug': 'proportion',
        'menu_order_start': 1,
        'subtopics': {
            'Ылдамдык, аралык жана убакыт': {'slug': 'speed-distance-time', 'subsubtopics': {}},
            'Түз жана тескери пропорция': {'slug': 'direct-inverse', 'subsubtopics': {}},
            'Айландыруу графиктери': {'slug': 'conversion-graphs', 'subsubtopics': {}},
            'Пайыздар: калькулятор менен': {
                'slug': 'percentages-calculator',
                'subsubtopics': {
                    'Туюнтуу': 'expressing',
                    'Чоңдуктун пайызы': 'percentage-of-a-quantity',
                    'Көбөйтүү жана азайтуу': 'increase-decrease',
                    'Кайталанма пайыздык өзгөрүү': 'repeated-percentage-change',
                },
            },
            'Катыш': {
                'slug': 'ratio',
                'subsubtopics': {
                    'Эквиваленттүүлүк': 'equivalence',
                    'Туюнтуу': 'expressing',
                    'Катыштар жана чоңдуктар': 'ratios-and-quantities',
                    'Түрлөндүрүү': 'manipulation',
                },
            },
            'Турмуштук колдонуулар': {
                'slug': 'real-life-applications',
                'subsubtopics': {
                    'Пайдалуу сатып алуу': 'best-buys',
                    'Валюта курстары': 'exchange-rates',
                    'Рецепттер': 'recipes',
                },
            },
        },
    },
    'Алгебра': {
        'slug': 'algebra',
        'menu_order_start': 1,
        'subtopics': {
            'Киришүү': {'slug': 'introduction', 'subsubtopics': {}},
            'Туюнтмаларды түзүү': {'slug': 'forming-expressions', 'subsubtopics': {}},
            'Теңдемелер: сызыктуу': {
                'slug': 'equations-linear',
                'subsubtopics': {
                    'Түзүү': 'forming',
                    'Белгисиз бир жагында': 'variable-on-one-side',
                    'Кашаа менен': 'with-brackets',
                    'Белгисиз эки жагында': 'variable-on-both-sides',
                },
            },
            'Теңдемелер: квадраттык': {
                'slug': 'equations-quadratic',
                'subsubtopics': {
                    'Көбөйтүүчүлөргө ажыратуу': 'factorisation',
                    'Ыкмалар': 'methods',
                },
            },
            'Теңдемелер: системасы': {
                'slug': 'equations-simultaneous',
                'subsubtopics': {
                    'Жоюу ыкмасы': 'elimination',
                    'Ыкмалар': 'methods',
                },
            },
            'Функциялар': {
                'slug': 'functions',
                'subsubtopics': {
                    'Түзүү': 'forming',
                    'Маанисин эсептөө': 'evaluating',
                },
            },
        },
    },
    'Геометрия': {
        'slug': 'geometry',
        'menu_order_start': 1,
        'subtopics': {
            'Бурчтар': {
                'slug': 'angles',
                'subsubtopics': {
                    'Негизги бурчтар': 'basic-angles',
                    'Параллель сызыктар': 'parallel-lines',
                    'Көп бурчтуктар': 'polygons',
                },
            },
            'Аянт, периметр жана көлөм': {
                'slug': 'area-perimeter-volume',
                'subsubtopics': {
                    'Аянт жана периметр': 'area-and-perimeter',
                    'Тегеректер': 'circles',
                    'Көлөм жана бет аянты': 'volume-and-surface-area',
                },
            },
            'Түрлөндүрүүлөр': {
                'slug': 'transformations',
                'subsubtopics': {
                    '2D түрлөндүрүүлөр': '2d-transformations',
                },
            },
            'Пифагор жана тригонометрия': {
                'slug': 'pythagoras-trigonometry',
                'subsubtopics': {
                    'Тик бурчтуу үч бурчтуктар': 'right-angled-triangles',
                    'Тик эмес бурчтуу үч бурчтуктар': 'non-right-angled-triangles',
                    'Тереңдетилген тригонометрия': 'advanced-trigonometry',
                },
            },
            'Векторлор': {
                'slug': 'vectors',
                'subsubtopics': {
                    'Векторлор менен эсептөөлөр': 'vector-arithmetic',
                    'Векторлук геометрия': 'vector-geometry',
                },
            },
            'Фигуралардын касиеттери': {
                'slug': 'properties-of-shapes',
                'subsubtopics': {
                    '2D жана 3D фигуралар': '2d-3d-shapes',
                    'Курулуштар жана геометриялык орундар': 'constructions-and-loci',
                },
            },
        },
    },
    'Ыктымалдуулук': {
        'slug': 'probability',
        'menu_order_start': 1,
        'subtopics': {
            'Негизги ыктымалдуулук': {
                'slug': 'basic-probability',
                'subsubtopics': {
                    'Жеке окуялар': 'single-events',
                },
            },
            'Айкалышкан окуялар': {
                'slug': 'combined-events',
                'subsubtopics': {
                    'Диаграммалар': 'diagrams',
                    'Дарак диаграммалары': 'tree-diagrams',
                },
            },
        },
    },
    'Дата': {
        'slug': 'statistics',
        'menu_order_start': 1,
        'subtopics': {
            'Орточо маанилер жана чачыроо': {
                'slug': 'averages-and-spread',
                'subsubtopics': {
                    'Негизги орточо маанилер': 'basic-averages',
                    'Жыштык таблицалары': 'frequency-tables',
                },
            },
            'Маалыматтарды сүрөттөө': {
                'slug': 'data-representation',
                'subsubtopics': {
                    'Диаграммалар жана графиктер': 'charts-and-graphs',
                    'Тереңдетилген маалымат сүрөттөө': 'advanced-data-representation',
                },
            },
            'Маалымат чогултуу': {
                'slug': 'data-collection',
                'subsubtopics': {
                    'Тандап алуу': 'sampling',
                },
            },
        },
    },
}


class Command(BaseCommand):
    help = (
        "Builds the Topic/Subtopic/Sub-subtopic content tree (translated "
        "to Kyrgyz) under the existing Сандар/Пропорция/Алгебра/Геометрия/"
        "Ыктымалдуулук/Дата menu items, and wires matching MenuItem "
        "entries so it's browsable from the nav. Idempotent - safe to "
        "re-run. Pass --undo to remove everything it adds; existing "
        "manually-added items (e.g. under "
        "Сандар) are never touched."
    )

    def add_arguments(self, parser):
        parser.add_argument('--undo', action='store_true')

    def handle(self, *args, **options):
        if options['undo']:
            self.undo()
        else:
            self.apply()

    def apply(self):
        for topic_title, topic_data in TAXONOMY.items():
            root_menu, _ = MenuItem.objects.get_or_create(
                title=topic_title, parent=None,
            )
            topic, created = Topic.objects.get_or_create(
                title=topic_title, defaults={'slug': topic_data['slug']},
            )
            if root_menu.topic_id != topic.id:
                root_menu.topic = topic
                root_menu.save(update_fields=['topic'])
            verb = 'Created' if created else 'Already exists'
            self.stdout.write(f"{verb} Topic: {topic_title}")

            order = topic_data['menu_order_start']
            for subtopic_title, subtopic_data in topic_data['subtopics'].items():
                subtopic, created = Subtopic.objects.get_or_create(
                    topic=topic, title=subtopic_title,
                    defaults={'slug': subtopic_data['slug']},
                )
                verb = 'Created' if created else 'Already exists'
                self.stdout.write(f"  {verb} Subtopic: {topic_title} > {subtopic_title}")

                subtopic_menu, _ = MenuItem.objects.get_or_create(
                    title=subtopic_title, parent=root_menu,
                    defaults={'order': order, 'topic': topic, 'subtopic': subtopic},
                )
                if subtopic_menu.topic_id != topic.id or subtopic_menu.subtopic_id != subtopic.id:
                    subtopic_menu.topic = topic
                    subtopic_menu.subtopic = subtopic
                    subtopic_menu.save(update_fields=['topic', 'subtopic'])
                order += 1

                for ss_order, (ss_title, ss_slug) in enumerate(
                    subtopic_data['subsubtopics'].items(), start=1
                ):
                    subsubtopic, created = SubSubtopic.objects.get_or_create(
                        subtopic=subtopic, title=ss_title, defaults={'slug': ss_slug},
                    )
                    verb = 'Created' if created else 'Already exists'
                    self.stdout.write(f"    {verb} Sub-subtopic: {subtopic_title} > {ss_title}")

                    ss_menu, _ = MenuItem.objects.get_or_create(
                        title=ss_title, parent=subtopic_menu,
                        defaults={
                            'order': ss_order, 'topic': topic,
                            'subtopic': subtopic, 'subsubtopic': subsubtopic,
                        },
                    )
                    if (
                        ss_menu.topic_id != topic.id
                        or ss_menu.subtopic_id != subtopic.id
                        or ss_menu.subsubtopic_id != subsubtopic.id
                    ):
                        ss_menu.topic = topic
                        ss_menu.subtopic = subtopic
                        ss_menu.subsubtopic = subsubtopic
                        ss_menu.save(update_fields=['topic', 'subtopic', 'subsubtopic'])

        self.stdout.write(self.style.SUCCESS('Done.'))

    def undo(self):
        # Root Topic-level MenuItems (Сандар/Пропорция/Алгебра) already
        # existed before this command and are never deleted - only the
        # Subtopic-level MenuItems this command created (and everything
        # under them, via cascade) are removed. Deleting the Topic rows
        # cascades to their Subtopics and SubSubtopics too.
        for topic_title, topic_data in TAXONOMY.items():
            subtopic_titles = list(topic_data['subtopics'].keys())
            deleted, _ = MenuItem.objects.filter(
                title__in=subtopic_titles, parent__title=topic_title, parent__parent__isnull=True,
            ).delete()
            if deleted:
                self.stdout.write(f"Removed menu branches under {topic_title}")

            topic_deleted, _ = Topic.objects.filter(title=topic_title).delete()
            if topic_deleted:
                self.stdout.write(f"Removed Topic (and its Subtopics/Sub-subtopics): {topic_title}")

        self.stdout.write(self.style.SUCCESS('Undo complete.'))
