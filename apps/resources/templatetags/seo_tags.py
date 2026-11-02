from django import template

from apps.resources.seo import (
    PAGES,
    apply_seo,
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
def seo_topic(context, name, grade=''):
    """A lesson or topic page. Grade is the stored badge, or the continuum."""
    grade = grade_for_request(context.get('request'), grade)
    title = topic_document_title(name, grade)
    description = topic_meta_description(name, grade)
    return apply_seo(
        context, title, description, 'topic', name=name or title, grade=grade,
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
