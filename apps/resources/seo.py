"""Document titles, descriptions, and JSON-LD for public pages.

Wording lives here so a title can be reviewed in one place. Topic pages
share one pattern. A stored grade (``5``, ``5 кл.``, ``5-кл.``,
``4-класс``, ``6–7 кл.``) is written in the title as ``N-класс`` or
``N–M-класс``. The badge drawn on the page is left as it is.
"""
import json
import re

from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.resources.continuum import continuum_for_href

SITE = 'MathKG'
DESCRIPTION_LIMIT = 160
# Search keywords only. There is no /ru/ site and no hreflang.
RU_PHRASE = 'Материалы по математике на кыргызском языке.'

# The visible title is Kyrgyz. Russian is only in the description tail,
# meta keywords, and JSON-LD alternateName.
HOME_TITLE = (
    'MathKG: математика мугалимдер жана ата-энелер үчүн окуу материалдары '
    '(презентация, иш барак)'
)
HOME_DESCRIPTION = (
    'Кыргызстандын мугалимдери үчүн даяр презентация жана иш барак. '
    + RU_PHRASE
)
HOME_KEYWORDS = (
    'математика для учителей, презентация, рабочий лист, '
    + RU_PHRASE.rstrip('.')
)

# key -> (title, description). Descriptions are written for a teacher
# or parent, and kept near 150 characters.
PAGES = {
    'about': (
        'MathKG жөнүндө | MathKG',
        'MathKG — кыргыз тилиндеги математика мугалимдер үчүн. ' + RU_PHRASE,
    ),
    'news': (
        'Сайттагы жаңылыктар | MathKG',
        'MathKG сайтындагы жаңы темалар жана оңдоолор. ' + RU_PHRASE,
    ),
    'pricing': (
        'Баалар | MathKG',
        'MathKG жазылуусу: 3 ай, 6 ай жана 1 жыл. ' + RU_PHRASE,
    ),
    'feedback': (
        'Пикир калтыруу | MathKG',
        'MathKG боюнча пикир, сунуш же мактоо калтырыңыз. ' + RU_PHRASE,
    ),
    'teacher_comments': (
        'Мугалимдердин пикирлери | MathKG',
        'Мугалимдердин MathKG жөнүндө жарыяланган пикирлери. ' + RU_PHRASE,
    ),
    'topics': (
        'Темалар дарагы | MathKG',
        'Темалар: сандар, алгебра, геометрия, ыктымалдуулук. ' + RU_PHRASE,
    ),
    'resources': (
        'Ресурстар | MathKG',
        'Презентация, иш барак жана тапшырмалар бир тизмеде. ' + RU_PHRASE,
    ),
    'tarsia': (
        'Тарсия куруучу | MathKG',
        'Өз сурооңуз менен тарсия табышмак түзүңүз. ' + RU_PHRASE,
    ),
    'big4': (
        'Төрт амал таймашы | MathKG',
        'Төрт амалды класста ойнотуучу таймаш. ' + RU_PHRASE,
    ),
    'login': (
        'Кирүү | MathKG',
        'MathKG аккаунтуңузга кириңиз. Катталган мугалим презентация, '
        'иш барак жана тапшырманы жүктөп алат.',
    ),
    'register': (
        'Катталуу | MathKG',
        'MathKG сайтына катталыңыз. 7 күн акысыз, андан кийин презентация, '
        'иш барак жана тапшырма жеткиликтүү болот.',
    ),
    'account': (
        'Аккаунт | MathKG',
        'Жазылууңуздун мөөнөтү жана аккаунт маалыматы. MathKG материалдарын '
        'жүктөп алуу ушул барактан көзөмөлдөнөт.',
    ),
    'check_email': (
        'Почтаңызды текшериңиз | MathKG',
        'Каттоо шилтемеси электрондук почтаңызга жөнөтүлдү. Ачкандан кийин '
        'материалдар 7 күн акысыз ачылат.',
    ),
    'resend': (
        'Активдештирүү шилтемеси | MathKG',
        'Каттоо каты келбесе, активдештирүү шилтемесин кайра сураңыз. '
        'MathKG аккаунтуңуз ошондон кийин ачылат.',
    ),
    'password_reset': (
        'Сырсөздү калыбына келтирүү | MathKG',
        'Сырсөздү унутуп калсаңыз, почтаңызды жазыңыз. Калыбына келтирүү '
        'шилтемесин MathKG ошол дарекке жөнөтөт.',
    ),
    'password_reset_done': (
        'Калыбына келтирүү каты | MathKG',
        'Эгер бул почта менен аккаунт бар болсо, сырсөздү калыбына келтирүү '
        'боюнча кат MathKG тарабынан жөнөтүлдү.',
    ),
    'password_reset_confirm': (
        'Жаңы сырсөз | MathKG',
        'MathKG аккаунтуңуз үчүн жаңы сырсөз орнотуңуз. Бул шилтеме бир '
        'жолу иштейт.',
    ),
    'password_reset_complete': (
        'Сырсөз жаңыртылды | MathKG',
        'Жаңы сырсөз сакталды. Эми MathKG аккаунтуңузга кирип, материалдарды '
        'ача аласыз.',
    ),
    'password_change': (
        'Сырсөздү өзгөртүү | MathKG',
        'Учурдагы сырсөздү жазып, MathKG аккаунтуңуз үчүн жаңы сырсөз коюңуз. '
        'Эски сырсөз иштебей калат.',
    ),
    'password_change_done': (
        'Сырсөз өзгөртүлдү | MathKG',
        'Сырсөзүңүз жаңырды. MathKG аккаунтуңуз эми жаңы сырсөз менен ачылат. Эски сырсөз иштебейт.',
    ),
    'registration_success': (
        'Катталуу аяктады | MathKG',
        'Аккаунт түзүлдү. Текшерүүдөн кийин MathKG презентация, иш барак '
        'жана тапшырмалары ачылат.',
    ),
    'dashboard': (
        'Башкаруу панели | MathKG',
        'Ресурстардын кыскача эсеби: файлдар, жүктөөлөр жана категориялар. '
        'Бул барак MathKG кызматкерлери үчүн.',
    ),
    'search': (
        'Издөө | MathKG',
        'Тема же материалдын атын жазыңыз. ' + RU_PHRASE,
    ),
    'kaitaloo': (
        'Кайталоо | MathKG',
        'Өтүлгөн теманы кайталоо үчүн MathKG материалдары: презентация, '
        'иш барак жана тапшырма.',
    ),
    'register_school': (
        'Мектеп жазылуусу | MathKG',
        'Мектеп үчүн MathKG жазылуусу. Мугалимдер презентация, иш барак '
        'жана тапшырманы бир аккаунттан ачат.',
    ),
}


def clean(value):
    return ' '.join(str(value or '').split())


def clip(text, limit=DESCRIPTION_LIMIT):
    text = clean(text)
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(' ', 1)[0]
    return cut.rstrip('.,;:—-– ') + '…'


def as_klass(label):
    """``5`` / ``5 кл.`` / ``5-кл.`` / ``4-класс`` -> ``5-класс``.

    A range stays a range: ``7–9`` and ``6–7 кл.`` become ``7–9-класс``
    and ``6–7-класс``. ``2–3, 5`` becomes ``2–3-класс, 5-класс``.
    """
    label = clean(label)
    if not label:
        return ''
    core = label
    for suffix in ('-класс', '-кл.', ' кл.', 'кл.'):
        if core.endswith(suffix):
            core = core[: -len(suffix)].strip()
            break
    parts = [part.strip() for part in core.split(',') if part.strip()]
    formatted = []
    for part in parts:
        match = re.fullmatch(r'(\d+)\s*[–-]\s*(\d+)', part)
        if match:
            formatted.append(f'{match.group(1)}–{match.group(2)}-класс')
        elif re.fullmatch(r'\d+', part):
            formatted.append(f'{part}-класс')
        else:
            return label
    return ', '.join(formatted)


def _one_russian(name):
    """A staff-edited title_ru wins. Otherwise the reviewed glossary."""
    from apps.resources.data.russian_names import RUSSIAN_NAMES

    try:
        from django.apps import apps
        if apps.ready:
            for label in ('personal.SubSubtopic', 'personal.Subtopic', 'personal.Topic'):
                model = apps.get_model(label)
                found = (
                    model.objects.filter(title=name)
                    .exclude(title_ru='')
                    .values_list('title_ru', flat=True)
                    .first()
                )
                if found:
                    return found
    except Exception:
        pass
    return RUSSIAN_NAMES.get(name, '')


def russian_name(name):
    """Russian search name for a Kyrgyz title, including ``A: B`` chains."""
    name = clean(name)
    if not name:
        return ''
    if ': ' in name:
        parts = [clean(part) for part in name.split(': ')]
        translated = [_one_russian(part) for part in parts]
        if not any(translated):
            return ''
        return ': '.join(ru or part for ru, part in zip(translated, parts))
    return _one_russian(name)


def topic_document_title(name, grade='', russian=''):
    """Visible title. Kyrgyz only, including the grade when we have one.

    ``russian`` is accepted and ignored so a caller cannot put it here.
    """
    del russian
    name = clean(name) or 'Тема'
    grade = as_klass(grade)
    if grade and grade not in name:
        heading = f'{name}, {grade}'
    else:
        heading = name
    return f'{heading}: презентация, иш барак, тапшырмалар | MathKG'


def topic_keywords(name):
    """Hidden search words. Not used in the title or on the page."""
    russian = russian_name(name)
    parts = [russian] if russian else []
    parts.append('презентация, рабочий лист')
    parts.append(RU_PHRASE.rstrip('.'))
    return ', '.join(parts)


def with_russian_phrase(kyrgyz):
    room = DESCRIPTION_LIMIT - len(RU_PHRASE) - 1
    return f'{clip(kyrgyz, room)} {RU_PHRASE}'


def topic_kyrgyz_sentence(name, grade=''):
    name = clean(name) or 'Бул тема'
    grade = as_klass(grade)
    if grade and grade not in name:
        lead = f'{name}, {grade}'
    else:
        lead = name
    return f'{lead}: презентация, иш барак жана тапшырмалар.'


def topic_meta_description(name, grade=''):
    return with_russian_phrase(topic_kyrgyz_sentence(name, grade))


def search_document_title(query):
    query = clean(query)
    if not query:
        return PAGES['search'][0]
    return clip(f'«{query}» боюнча издөө | MathKG', 120)


def search_meta_description(query):
    query = clean(query)
    if not query:
        return PAGES['search'][1]
    return with_russian_phrase(f'«{query}» боюнча темалар жана материалдар.')


def grade_for_request(request, explicit=''):
    """Grade for a title.

    The badge passed in from the page wins, so the title matches the
    chip on the page. Otherwise the menu grade (a pack grade, else the
    Kyrgyz-programme audit in menu_grades.py). Otherwise the 12-year
    continuum band.
    """
    explicit = clean(explicit)
    if explicit:
        return as_klass(explicit)
    if request is None:
        return ''
    path = getattr(request, 'path', '') or ''
    if path and not path.endswith('/'):
        path += '/'
    from apps.resources.data.menu_grades import grade_for_url
    menu = grade_for_url(path) if path else ''
    if menu:
        return as_klass(menu)
    nav = continuum_for_href(path)
    if not nav:
        return ''
    return as_klass(nav.get('grade_band'))


def canonical_url(request):
    path = request.path or '/'
    match = getattr(request, 'resolver_match', None)
    # /home/ renders the same page as /. One canonical.
    if match is not None and match.url_name == 'home':
        path = '/'
    return request.build_absolute_uri(path)


def seo_context(request):
    """Defaults. A page's {% seo_page %} / {% seo_topic %} replaces them."""
    return {
        'seo_title': SITE,
        'seo_description': HOME_DESCRIPTION,
        'seo_canonical': canonical_url(request),
        'seo_image': request.build_absolute_uri(static('img/logo.jpg')),
        'seo_jsonld': '',
    }


def _origin(canonical):
    # https://host/path -> https://host
    parts = canonical.split('/', 3)
    return '/'.join(parts[:3]) if len(parts) >= 3 else canonical


def json_ld(data):
    raw = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    raw = raw.replace('&', r'\u0026').replace('<', r'\u003c').replace('>', r'\u003e')
    return mark_safe(
        '<script type="application/ld+json">' + raw + '</script>'
    )


def home_jsonld_with_logo(canonical, image):
    origin = _origin(canonical)
    kyrgyz = (
        'Кыргызстандын мугалимдери үчүн даяр презентация жана иш барак.'
    )
    return json_ld({
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Organization',
                'name': SITE,
                'alternateName': 'Математика для учителей',
                'url': origin + '/',
                'logo': image,
                'email': 'mathematicskgz@gmail.com',
                'areaServed': 'KG',
                'description': kyrgyz,
            },
            {
                '@type': 'WebSite',
                'name': SITE,
                'alternateName': 'Математика для учителей',
                'url': origin + '/',
                'inLanguage': 'ky',
                'description': kyrgyz,
                'publisher': {'@type': 'Organization', 'name': SITE},
                'potentialAction': {
                    '@type': 'SearchAction',
                    'target': origin + '/search/?q={search_term_string}',
                    'query-input': 'required name=search_term_string',
                },
            },
        ],
    })


def learning_resource_jsonld(canonical, name, description, grade, image, alternate_name=''):
    origin = _origin(canonical)
    data = {
        '@context': 'https://schema.org',
        '@type': 'LearningResource',
        'name': name,
        'description': description,
        'url': canonical,
        'inLanguage': 'ky',
        'learningResourceType': ['Презентация', 'Иш барак', 'Тапшырма'],
        'audience': {
            '@type': 'EducationalAudience',
            'educationalRole': ['teacher', 'parent'],
        },
        'provider': {
            '@type': 'Organization',
            'name': SITE,
            'url': origin + '/',
            'logo': image,
        },
    }
    if grade:
        data['educationalLevel'] = grade
    alternate_name = clean(alternate_name)
    if alternate_name:
        data['alternateName'] = alternate_name
    return json_ld(data)


def head_tags(title, description, canonical, image, jsonld, keywords=''):
    """The document title and social tags. Returned as HTML because a
    {% block %} renders in a copied context, so values set inside it
    do not reach the rest of the base template.

    ``keywords`` is the only place a Russian topic name is written into
    the head, besides the description tail and JSON-LD alternateName.
    """
    keyword_tag = ''
    if keywords:
        keyword_tag = format_html(
            '<meta name="keywords" content="{keywords}">\n',
            keywords=keywords,
        )
    return format_html(
        '<title>{title}</title>\n'
        '<meta name="description" content="{description}">\n'
        '{keywords}'
        '<link rel="canonical" href="{canonical}">\n'
        '<meta property="og:title" content="{title}">\n'
        '<meta property="og:description" content="{description}">\n'
        '<meta property="og:url" content="{canonical}">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:locale" content="ky_KG">\n'
        '<meta property="og:site_name" content="MathKG">\n'
        '<meta property="og:image" content="{image}">\n'
        '<meta property="og:image:alt" content="MathKG">\n'
        '{jsonld}\n',
        title=title,
        description=description,
        keywords=keyword_tag,
        canonical=canonical,
        image=image,
        jsonld=jsonld,
    )


def apply_seo(context, title, description, kind, name='', grade=''):
    request = context['request']
    canonical = canonical_url(request)
    image = request.build_absolute_uri(static('img/logo.jpg'))
    keywords = ''
    if kind == 'home':
        jsonld = home_jsonld_with_logo(canonical, image)
        keywords = HOME_KEYWORDS
    elif kind == 'topic':
        kyrgyz_name = name or title
        russian = russian_name(kyrgyz_name)
        jsonld = learning_resource_jsonld(
            canonical,
            kyrgyz_name,
            topic_kyrgyz_sentence(kyrgyz_name, grade),
            grade,
            image,
            alternate_name=russian,
        )
        keywords = topic_keywords(kyrgyz_name)
    else:
        jsonld = ''
    return head_tags(title, description, canonical, image, jsonld, keywords)
