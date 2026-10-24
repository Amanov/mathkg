# apps/resources/views/context_processors.py

from apps.resources.models import MenuItem


def menu_items(request):
    return {
        "menu_items": MenuItem.objects.filter(
            parent__isnull=True
        ).prefetch_related(
            "children",
            "children__children",
            "children__children__children", "children__children__children__children"
        ).order_by('order')
    }


def topic_continuum(request):
    from apps.resources.continuum import continuum_for_path

    return {'topic_continuum': continuum_for_path(getattr(request, 'path', ''))}