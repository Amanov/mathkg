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
TOPIC_TAIL = ': презентация, иш барак, тапшырмалар | MathKG'
DESCRIPTION_LIMIT = 160

# The home title is the wording asked for. The rest of the site usually
# says «мугалимдери»; this line says «мугалимдер». Kept exact on purpose.
HOME_TITLE = (
    'MathKG: математика мугалимдер жана ата-энелер үчүн окуу материалдары '
    '(презентация, иш барак)'
)
HOME_DESCRIPTION = (
    'Кыргызстандын мугалимдери жана ата-энелери үчүн даяр математика: '
    'презентация, иш барак жана тапшырма. Сабакты бир жерден ачып, класска алып кириңиз.'
)

# key -> (title, description). Descriptions are written for a teacher
# or parent, and kept near 150 characters.
PAGES = {
    'about': (
        'MathKG жөнүндө | MathKG',
        'MathKG — кыргыз тилиндеги математика платформасы. Мугалимдер '
        'менен ата-энелер үчүн презентация, иш барак жана тапшырма бир жерде.',
    ),
    'news': (
        'Сайттагы жаңылыктар | MathKG',
        'MathKG сайтына кошулган өзгөрүүлөр: жаңы темалар, материалдар '
        'жана оңдоолор. Мугалим үчүн кыскача баяндама.',
    ),
    'pricing': (
        'Баалар | MathKG',
        'MathKG жазылуусунун баасы: 3 ай, 6 ай жана 1 жыл. Презентация, '
        'иш барак жана тапшырманы канча жолу жүктөөгө болору жазылган.',
    ),
    'topics': (
        'Темалар дарагы | MathKG',
        'Математиканын темалары бир тизмеде: сандар, алгебра, геометрия, '
        'ыктымалдуулук жана статистика. MathKG.',
    ),
    'resources': (
        'Ресурстар | MathKG',
        'Презентация, иш барак жана мугалим жетектеген тапшырмалар. '
        'MathKG китепканасынан материалды категория боюнча табыңыз.',
    ),
    'tarsia': (
        'Тарсия куруучу | MathKG',
        'Өз сурооңузду жазып, кесип-жанаштыруучу тарсия табышмак түзүңүз. '
        'Класста колдонууга даяр файлды жүктөп алыңыз.',
    ),
    'big4': (
        'Big 4 сан таймашы | MathKG',
        'Төрт амалды класста ойнотуучу таймаш. Мугалим тактадан суроо '
        'көрсөтөт, окуучулар жооп берет. MathKG.',
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
        'Тема же материалдын атын жазыңыз. MathKG презентация, иш барак '
        'жана тапшырмалардын арасынан издейт.',
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


def topic_document_title(name, grade=''):
    name = clean(name) or 'Тема'
    grade = as_klass(grade)
    if grade and grade not in name:
        heading = f'{grade} — {name}'
    else:
        heading = name
    return heading + TOPIC_TAIL


def topic_meta_description(name, grade=''):
    name = clean(name) or 'Бул тема'
    grade = as_klass(grade)
    if grade and grade not in name:
        lead = f'{name} ({grade})'
    else:
        lead = name
    return clip(
        f'{lead}: презентация, иш барак жана тапшырмалар. '
        f'Мугалимдер менен ата-энелер үчүн даяр материал MathKG сайтында.'
    )


def search_document_title(query):
    query = clean(query)
    if not query:
        return PAGES['search'][0]
    return clip(f'«{query}» боюнча издөө | MathKG', 120)


def search_meta_description(query):
    query = clean(query)
    if not query:
        return PAGES['search'][1]
    return clip(
        f'«{query}» боюнча темалар жана материалдар. Презентация, иш барак '
        f'жана тапшырмалар MathKG сайтында.'
    )


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
    return json_ld({
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Organization',
                'name': SITE,
                'url': origin + '/',
                'logo': image,
                'email': 'mathematicskgz@gmail.com',
                'areaServed': 'KG',
                'description': HOME_DESCRIPTION,
            },
            {
                '@type': 'WebSite',
                'name': SITE,
                'url': origin + '/',
                'inLanguage': 'ky',
                'description': HOME_DESCRIPTION,
                'publisher': {'@type': 'Organization', 'name': SITE},
                'potentialAction': {
                    '@type': 'SearchAction',
                    'target': origin + '/search/?q={search_term_string}',
                    'query-input': 'required name=search_term_string',
                },
            },
        ],
    })


def learning_resource_jsonld(canonical, name, description, grade, image):
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
    return json_ld(data)


def head_tags(title, description, canonical, image, jsonld):
    """The document title and social tags. Returned as HTML because a
    {% block %} renders in a copied context, so values set inside it
    do not reach the rest of the base template."""
    return format_html(
        '<title>{title}</title>\n'
        '<meta name="description" content="{description}">\n'
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
        canonical=canonical,
        image=image,
        jsonld=jsonld,
    )


def apply_seo(context, title, description, kind, name='', grade=''):
    request = context['request']
    canonical = canonical_url(request)
    image = request.build_absolute_uri(static('img/logo.jpg'))
    if kind == 'home':
        jsonld = home_jsonld_with_logo(canonical, image)
    elif kind == 'topic':
        jsonld = learning_resource_jsonld(
            canonical, name or title, description, grade, image,
        )
    else:
        jsonld = ''
    return head_tags(title, description, canonical, image, jsonld)
