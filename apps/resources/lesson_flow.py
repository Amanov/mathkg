"""Lesson-flow navigation: the 5E + 3C teaching model, each stage tied to
the Bloom's taxonomy levels it mainly works on.

The landing page, the "Сабак куруу" row in the header and the
/sabak/<stage>/ pages all read from STAGES here, so the model is defined
once. Materials are not tagged in the database by stage - they are
sorted into stages by what kind of activity they are (block title /
section header on the data-file pages, learning_goal / activity_type on
Resource rows), using the rules below.
"""

from django.urls import NoReverseMatch, reverse

from apps.resources.data.adding_subtracting_1_digit_data import ADDING_SUBTRACTING_1_DIGIT_SECTIONS
from apps.resources.data.algebra_linear_data import ALGEBRA_LINEAR_VAR1SIDE_NONCALC_1STEP_SECTIONS
from apps.resources.data.all_operations_data import ALL_OPERATIONS_SECTIONS
from apps.resources.data.directed_numbers_data import DIRECTED_NUMBERS_SECTIONS
from apps.resources.data.four_basic_operations_data import FOUR_BASIC_OPERATIONS_SECTIONS
from apps.resources.data.koshuu_1_digit_data import KOSHUU_1_DIGIT_SECTIONS
from apps.resources.data.subtracting_1_digit_data import SUBTRACTING_1_DIGIT_SECTIONS


# Bloom's taxonomy, lowest to highest.
BLOOM_LEVELS = [
    {
        'key': 'remember', 'number': 1, 'name': 'Эстеп калуу',
        'stems': ['... деген эмне?', 'Эрежесин айтып бер.', 'Мисалдарды тизмеле.'],
    },
    {
        'key': 'understand', 'number': 2, 'name': 'Түшүнүү',
        'stems': ['Өз сөзүң менен түшүндүр.', 'Эмне үчүн мындай болот?', 'Сүрөт менен көрсөт.'],
    },
    {
        'key': 'apply', 'number': 3, 'name': 'Колдонуу',
        'stems': ['Бул ыкма менен чыгар.', 'Жоопту тап жана текшер.', 'Турмуштук маселеге колдон.'],
    },
    {
        'key': 'analyze', 'number': 4, 'name': 'Талдоо',
        'stems': ['Эмнеси окшош, эмнеси айырмаланат?', 'Кайсы кадамда ката кетти?', 'Топторго бөл.'],
    },
    {
        'key': 'evaluate', 'number': 5, 'name': 'Баалоо',
        'stems': ['Кайсы жооп туура? Негизде.', 'Бул чечим эң ыңгайлуубу?', 'Макулсуңбу? Эмне үчүн?'],
    },
    {
        'key': 'create', 'number': 6, 'name': 'Жаратуу',
        'stems': ['Ушул жооп чыга турган маселе түз.', 'Өз ыкмаңды сунушта.', 'Досуң үчүн суроо түз.'],
    },
]
BLOOM_BY_KEY = {level['key']: level for level in BLOOM_LEVELS}


STAGES = [
    # ── 5E: the order a lesson actually runs in ──────────────────────
    {
        'slug': 'kyzyktyruu', 'group': '5e', 'number': 1,
        'name': 'Кызыктыруу', 'name_en': 'Engage', 'icon': 'fa-lightbulb',
        'bloom': ['remember'],
        'summary': 'Мурунку билимди эске салып, сабакка кызыгууну ойготуу.',
        'teacher_does': 'Тактага кыска суроо чыгарып, бүт класстын жообун тез көрөсүз.',
        'activity_types': ['Тактадагы суроолор', '1-2-3-4', 'Мага көрсөт', 'Жеңил, орто, оор'],
    },
    {
        'slug': 'izildoo', 'group': '5e', 'number': 2,
        'name': 'Изилдөө', 'name_en': 'Explore', 'icon': 'fa-magnifying-glass',
        'bloom': ['understand'],
        'summary': 'Окуучулар өздөрү байкап, мыйзамченемдүүлүктү табышат.',
        'teacher_does': 'Табышмак же ачык тапшырма берип, окуучулардын ойлорун угасыз.',
        'activity_types': ['Цифралык табышмак', '100 чарчы', 'Кутучалар'],
    },
    {
        'slug': 'tushunduruu', 'group': '5e', 'number': 3,
        'name': 'Түшүндүрүү', 'name_en': 'Explain', 'icon': 'fa-person-chalkboard',
        'bloom': ['understand', 'apply'],
        'summary': 'Жаңы түшүнүктү көрсөтмө мисалдар менен ачып берүү.',
        'teacher_does': 'Даяр презентация менен мисалды кадам-кадамы менен көрсөтөсүз.',
        'activity_types': ['Сабактын презентациясы', 'Мисал көрсөт'],
    },
    {
        'slug': 'terendetuu', 'group': '5e', 'number': 4,
        'name': 'Тереңдетүү', 'name_en': 'Elaborate', 'icon': 'fa-layer-group',
        'bloom': ['apply', 'analyze'],
        'summary': 'Билимди жаңы маселелерде бышыктоо, деңгээл боюнча машыгуу.',
        'teacher_does': 'Иш баракты басып чыгарып, окуучулар өз деңгээлинде иштешет.',
        'activity_types': ['Иш барактар', 'Тарсия курак', 'Жооп торчосу', 'Төрт катар'],
    },
    {
        'slug': 'baaloo', 'group': '5e', 'number': 5,
        'name': 'Баалоо', 'name_en': 'Evaluate', 'icon': 'fa-clipboard-check',
        'bloom': ['evaluate'],
        'summary': 'Түшүнүүнү текшерүү жана кийинки кадамды чечүү.',
        'teacher_does': 'Катаны табуу же туура/ката тапшырмасы менен сабакты жыйынтыктайсыз.',
        'activity_types': ['Катаны тап', 'Туура же ката лабиринт', 'Чечим чыгаруу'],
    },
    # ── 3C: run through every stage rather than at one point in it ───
    {
        'slug': 'bailanyshtyruu', 'group': '3c', 'number': 1,
        'name': 'Байланыштыруу', 'name_en': 'Connect', 'icon': 'fa-link',
        'bloom': ['analyze'],
        'summary': 'Түшүнүктөрдү бири-бирине жана турмушка байланыштыруу.',
        'teacher_does': 'Карталарды салыштырып, топтоп, жуптарды табуу тапшырмасын бересиз.',
        'activity_types': ['Салыштыруу', '3кө туташтыруу', 'Карта сорттоо'],
    },
    {
        'slug': 'kyzmattashuu', 'group': '3c', 'number': 2,
        'name': 'Кызматташуу', 'name_en': 'Collaborate', 'icon': 'fa-people-group',
        'bloom': ['apply', 'analyze'],
        'summary': 'Топтук жана жуп менен иштөө, мугалим жетектеген оюндар.',
        'teacher_does': 'Класс командаларга бөлүнүп, оюн аркылуу маселе чыгарат.',
        'activity_types': ['Бинго', 'Жыдымай', 'Х жана О', 'Блокбастер', 'Айып сокку'],
    },
    {
        'slug': 'jaratuu', 'group': '3c', 'number': 3,
        'name': 'Жаратуу', 'name_en': 'Create', 'icon': 'fa-pen-ruler',
        'bloom': ['create'],
        'summary': 'Окуучулар өз суроосун, маселесин же далилин түзүшөт.',
        'teacher_does': 'Жоопту берип, окуучулардан ага ылайык маселе түзүүнү сурайсыз.',
        'activity_types': ['Суроо түз', 'Далилдөө'],
    },
]
STAGE_BY_SLUG = {stage['slug']: stage for stage in STAGES}


# Block title (or, failing that, section header) keyword -> stage slug.
# First match wins, so the more specific phrases come first.
TITLE_RULES = [
    ('көрсөтүү - түшүндүрүү', 'tushunduruu'),
    ('мисал көрсөт', 'tushunduruu'),
    ('мага көрсөт', 'kyzyktyruu'),
    ('1-2-3-4', 'kyzyktyruu'),
    ('1234', 'kyzyktyruu'),
    ('жеңил, орто, оор', 'kyzyktyruu'),
    ('цифралык табышмак', 'izildoo'),
    ('100 чарчы', 'izildoo'),
    ('кутучалар', 'izildoo'),
    ('катаны тап', 'baaloo'),
    ('туура же ката', 'baaloo'),
    ('чечим чыгаруу', 'baaloo'),
    ('салыштыруу', 'bailanyshtyruu'),
    ('туташтыруу', 'bailanyshtyruu'),
    ('сорттоо', 'bailanyshtyruu'),
    ('бинго', 'kyzmattashuu'),
    ('жыдымай', 'kyzmattashuu'),
    ('х жана о', 'kyzmattashuu'),
    ('блокбастер', 'kyzmattashuu'),
    ('айып сокку', 'kyzmattashuu'),
    ('суроо түз', 'jaratuu'),
    ('тарсия', 'terendetuu'),
    ('жооп торчосу', 'terendetuu'),
    ('төрт катар', 'terendetuu'),
    ('көнүгүү', 'terendetuu'),
    ('көндүм', 'terendetuu'),
]
HEADER_RULES = [
    ('оюн', 'kyzmattashuu'),
    ('ойун', 'kyzmattashuu'),
    ('презентация', 'tushunduruu'),
    ('көрсөтмө', 'tushunduruu'),
    ('киришүү', 'tushunduruu'),
    ('тактада', 'kyzyktyruu'),
    ('иш барак', 'terendetuu'),
]

# Resource rows (topic tree) carry their own tags.
LEARNING_GOAL_STAGE = {
    'retrieval': 'kyzyktyruu',
    'patterns': 'izildoo',
    'visuals': 'izildoo',
    'discovery': 'izildoo',
    'presentation': 'tushunduruu',
    'fluency': 'terendetuu',
    'problem_solving': 'terendetuu',
    'discussion': 'kyzmattashuu',
    'games': 'kyzmattashuu',
    'modelling': 'bailanyshtyruu',
    'proof': 'jaratuu',
}
ACTIVITY_TYPE_STAGE = {
    'show_me': 'kyzyktyruu',
    'abc': 'kyzyktyruu',
    'digit_puzzle': 'izildoo',
    'lesson': 'tushunduruu',
    'answer_grid': 'terendetuu',
    'four_in_row': 'terendetuu',
    'worded': 'terendetuu',
    'answer_maze': 'baaloo',
    'true_false_maze': 'baaloo',
    'card_match': 'bailanyshtyruu',
    'card_sort': 'bailanyshtyruu',
    'link': 'bailanyshtyruu',
    'create_question': 'jaratuu',
}
CATEGORY_STAGE = {
    'presentation': 'tushunduruu',
    'worksheet': 'terendetuu',
    'activity': 'kyzmattashuu',
}

# The hand-built pages whose materials live in apps/resources/data/.
DATA_PAGES = [
    ('four_basic_operations', 'Төрт амал', FOUR_BASIC_OPERATIONS_SECTIONS),
    ('all_operations', 'Аралаш амалдар', ALL_OPERATIONS_SECTIONS),
    ('directed_numbers', 'Багытталган сандар', DIRECTED_NUMBERS_SECTIONS),
    ('koshuu_1_digit', 'Кошуу — 1 орундуу сандар', KOSHUU_1_DIGIT_SECTIONS),
    ('subtracting_1_digit', 'Кемитүү — 1 орундуу сандар', SUBTRACTING_1_DIGIT_SECTIONS),
    ('adding_subtracting_1_digit', 'Кошуу жана кемитүү — 1 орундуу сандар', ADDING_SUBTRACTING_1_DIGIT_SECTIONS),
    ('algebra_linear_var1side_noncalc_1step', 'Белгисиз бир жагында: 1-кадам', ALGEBRA_LINEAR_VAR1SIDE_NONCALC_1STEP_SECTIONS),
]


def _match(text, rules):
    text = (text or '').lower()
    for keyword, slug in rules:
        if keyword in text:
            return slug
    return None


def classify_block(title, header):
    return _match(title, TITLE_RULES) or _match(header, HEADER_RULES) or 'terendetuu'


def _sentence_case(text):
    text = text.strip()
    return text[:1].upper() + text[1:]


def _file_formats(files):
    """['x.pptx', 'xA4.pdf', 'xA5.pdf'] -> ['PPT', 'PDF A4', 'PDF A5']."""
    formats = []
    for name in files:
        stem, _, ext = name.rpartition('.')
        ext = ext.lower()
        if ext == 'pptx':
            label = 'PPT'
        else:
            label = ext.upper()
            for size in ('A3', 'A4', 'A5', 'A6'):
                if stem.endswith(size):
                    label = f'{label} {size}'
                    break
        if label not in formats:
            formats.append(label)
    return formats


def _stage_card_fields(slug):
    stage = STAGE_BY_SLUG[slug]
    return {
        'stage': stage,
        'bloom': [BLOOM_BY_KEY[key] for key in stage['bloom']],
    }


def _data_page_materials():
    items = []
    for url_name, page_title, sections in DATA_PAGES:
        try:
            page_url = reverse(url_name)
        except NoReverseMatch:
            continue
        for section in sections:
            header = section.get('header', '')
            for block in section.get('blocks', []):
                slug = classify_block(block.get('title'), header)
                items.append({
                    'title': _sentence_case(block.get('title', '')),
                    'subtitle': block.get('subtitle', ''),
                    'page_title': page_title,
                    'url': page_url,
                    'image': block.get('fallback_image') or '',
                    'image_is_static': True,
                    'formats': _file_formats(block.get('files', [])),
                    **_stage_card_fields(slug),
                })
    return items


def _resource_url(resource):
    try:
        if resource.subsubtopic_id:
            return reverse('subsubtopic_detail', args=[
                resource.topic.slug, resource.subtopic.slug, resource.subsubtopic.slug,
            ])
        if resource.subtopic_id:
            return reverse('subtopic_detail', args=[resource.topic.slug, resource.subtopic.slug])
        return reverse('topic_detail', args=[resource.topic.slug])
    except NoReverseMatch:
        return None


def _topic_resource_materials():
    from apps.resources.models import Resource

    items = []
    resources = (
        Resource.objects.filter(is_active=True, topic__isnull=False)
        .select_related('topic', 'subtopic', 'subsubtopic')
    )
    for resource in resources:
        url = _resource_url(resource)
        if not url:
            continue
        slug = (
            ACTIVITY_TYPE_STAGE.get(resource.activity_type)
            or LEARNING_GOAL_STAGE.get(resource.learning_goal)
            or CATEGORY_STAGE.get(resource.category, 'terendetuu')
        )
        place = resource.subsubtopic or resource.subtopic or resource.topic
        items.append({
            'title': resource.title,
            'subtitle': '',
            'page_title': place.title,
            'url': url,
            'image': resource.image.url if resource.image else '',
            'image_is_static': False,
            'formats': _file_formats([resource.file.name]) if resource.file else [],
            **_stage_card_fields(slug),
        })
    return items


def all_materials():
    return _data_page_materials() + _topic_resource_materials()


def stages_with_counts(materials):
    counts = {}
    for item in materials:
        slug = item['stage']['slug']
        counts[slug] = counts.get(slug, 0) + 1
    result = []
    for stage in STAGES:
        result.append({
            **stage,
            'count': counts.get(stage['slug'], 0),
            'bloom_levels': [BLOOM_BY_KEY[key] for key in stage['bloom']],
        })
    return result


def lesson_nav(request):
    """Context processor: the 5E + 3C stages for the header row."""
    stages = [
        {**stage, 'bloom_levels': [BLOOM_BY_KEY[key] for key in stage['bloom']]}
        for stage in STAGES
    ]
    return {
        'lesson_nav_5e': [s for s in stages if s['group'] == '5e'],
        'lesson_nav_3c': [s for s in stages if s['group'] == '3c'],
    }
