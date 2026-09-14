# apps/resources/views/context_processors.py

from apps.resources.models import Topic, MenuItem


def topic_menu(request):
    return {
        "menu_topics": Topic.objects.prefetch_related(
            'subtopics',
            'subtopics__subsubtopics'
        )
    }


def menu_items(request):
    return {
        "menu_items": MenuItem.objects.filter(
            parent__isnull=True          # ← use isnull=True, not parent=None
        ).prefetch_related(
            "children",
            "children__children",
            "children__children__children", "children__children__children__children"
        ).order_by('order')
    }

# !! DELETE these lines — they run on every server start and pollute your DB !!
# MenuItem.objects.filter(url_name='tort_amal').update(...)
# MenuItem.objects.filter(url_name='bagyttalgan_sandar_amaldar').update(...)
# MenuItem.objects.filter(url_name='aralash_amaldar').update(...)