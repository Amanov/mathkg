# apps/resources/views/context_processors.py

from apps.resources.models import MenuItem
from apps.resources.reactions import VOTED_COOKIE, path_token


def root_menu(*, full):
    """Top-level items. The home page only needs one level so it can
    draw the bar. The menu fragment asks for the whole tree."""
    query = MenuItem.objects.filter(parent__isnull=True).order_by('order')
    if full:
        return query.prefetch_related(
            'children',
            'children__children',
            'children__children__children',
            'children__children__children__children',
        )
    return query.prefetch_related('children')


def menu_items(request):
    return {'menu_items': root_menu(full=False)}


def reaction_state(request):
    """Whether this browser already sent a face for the current page.

    Reads the vote cookie only. No database query, so the row stays cheap
    on every page.
    """
    path = getattr(request, 'path', '') or '/'
    raw = request.COOKIES.get(VOTED_COOKIE, '')
    return {'reaction_done': path_token(path) in raw.split('.')}