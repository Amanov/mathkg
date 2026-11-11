from django import template

from apps.resources.seo import (
    PAGES,
    apply_seo,
    grade_page_description,
    grade_page_title,
    grade_for_request,
    search_document_title,
    search_meta_description,
    topic_document_title,
    topic_meta_description,
    HOME_DESCRIPTION,
    HOME_TITLE,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def seo_page(context, key):
    """A named public page. Copy is apps.resources.seo.PAGES."""
    if key == 'home':
        title, description = HOME_TITLE, HOME_DESCRIPTION
        kind = 'home'
    else:
        title, description = PAGES[key]
        kind = 'page'
    return apply_seo(context, title, description, kind)


@register.simple_tag(takes_context=True)
def seo_topic(context, name, grade='', canonical_path='', breadcrumb=None):
    """A lesson or topic page. Grade is the stored badge, or the continuum.
    Pack pages also pass their main URL and their linked path."""
    grade = grade_for_request(context.get('request'), grade)
    title = topic_document_title(name, grade)
    description = topic_meta_description(name, grade)
    return apply_seo(
        context, title, description, 'topic', name=name or title, grade=grade,
        canonical_path=canonical_path, breadcrumb=breadcrumb,
    )


@register.simple_tag(takes_context=True)
def seo_topic_parts(context, part_a, part_b='', part_c='', grade=''):
    """Most specific name, then its parents, joined for a unique title."""
    parts = []
    for part in (part_a, part_b, part_c):
        text = ' '.join(str(part or '').split())
        if text and text not in parts:
            parts.append(text)
    name = ': '.join(parts)
    return seo_topic(context, name, grade)


@register.simple_tag(takes_context=True)
def seo_search(context, query=''):
    title = search_document_title(query)
    description = search_meta_description(query)
    return apply_seo(context, title, description, 'page')


@register.simple_tag(takes_context=True)
def seo_grade(context, grade):
    """A class page such as /4-klass/."""
    return apply_seo(
        context, grade_page_title(grade), grade_page_description(grade),
        'grade', grade=grade,
    )


@register.simple_tag
def grade_page_links():
    """Class numbers that have a /N-klass/ page, for the footer."""
    from apps.resources.grade_search import grade_page_numbers
    return grade_page_numbers()
