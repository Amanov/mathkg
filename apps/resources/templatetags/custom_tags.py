from django import template
from django.urls import reverse, NoReverseMatch

from ..models import MenuItem

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def safe_url(url_name):
    """
    Reverse a URL name the way {% url %} does, but degrade to '#' instead
    of raising NoReverseMatch. MenuItem.url_name is free-text data entered
    through the admin; the menu itself renders via a context processor on
    every single page, so one MenuItem pointing at a URL name that needs
    arguments (or that no longer exists) would otherwise 500 the entire
    site rather than just that one link.
    """
    if not url_name:
        return '#'
    try:
        return reverse(url_name)
    except NoReverseMatch:
        return '#'


@register.simple_tag
def menu_item_url(item):
    """A MenuItem's link: its Topic/Subtopic/Sub-subtopic pick if it has
    one (the most specific level set), else its plain url_name, else '#'."""
    resolved = item.get_resolved_url()
    if resolved:
        return resolved
    return safe_url(item.url_name)


def _is_content_item(item):
    """A MenuItem that is an actual page, not just a category/chevron
    node that exists only to group its children."""
    return bool(item.url_name) or item.topic_id is not None


def _current_menu_item(request):
    """Find the MenuItem for the page `request` resolved to, or None if
    this page isn't one (home, login, dashboards, admin-only views, ...)."""
    match = request.resolver_match
    if match is None:
        return None

    if match.url_name in ('topic_detail', 'subtopic_detail', 'subsubtopic_detail'):
        topic_slug = match.kwargs.get('topic_slug')
        subtopic_slug = match.kwargs.get('subtopic_slug')
        subsubtopic_slug = match.kwargs.get('subsubtopic_slug')
        if not topic_slug:
            return None
        return MenuItem.objects.filter(
            topic__slug=topic_slug,
            subtopic__slug=subtopic_slug if subtopic_slug else None,
            subsubtopic__slug=subsubtopic_slug if subsubtopic_slug else None,
        ).select_related('parent').first()

    if match.url_name:
        return MenuItem.objects.filter(
            url_name=match.url_name
        ).select_related('parent').first()

    return None


@register.inclusion_tag('snippets/related_topics.html', takes_context=True)
def related_topics(context):
    """Prev/next sibling navigation, shown just before the footer on every
    real leaf/content page (base/base.html). Renders nothing on any page
    that isn't a content page reachable from the menu tree, or that has
    no content siblings to link to."""
    request = context.get('request')
    if request is None:
        return {}

    current = _current_menu_item(request)
    if current is None or current.parent_id is None:
        return {}

    siblings = [
        item for item in MenuItem.objects.filter(
            parent_id=current.parent_id
        ).order_by('order', 'id')
        if item.pk == current.pk or _is_content_item(item)
    ]

    try:
        index = next(i for i, item in enumerate(siblings) if item.pk == current.pk)
    except StopIteration:
        return {}

    prev_item = siblings[index - 1] if index > 0 else None
    next_item = siblings[index + 1] if index < len(siblings) - 1 else None

    if prev_item is None and next_item is None:
        return {}

    return {'prev_item': prev_item, 'next_item': next_item}
