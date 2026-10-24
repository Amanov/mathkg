"""The ten Singapore-continuum bridge pages.

Routes are generated from ``data/bridge/pages/*.json``, so a new slug
appears here as soon as its spec file does. Each name is argument-free
so a MenuItem can point at it with ``url_name``.
"""

from django.urls import path

from apps.resources.bridge_pages import iter_pages
from apps.resources.views.bridge import bridge_topic_view

urlpatterns = [
    path(
        f"{page['slug']}/",
        bridge_topic_view,
        {'slug': page['slug']},
        name=page['url_name'],
    )
    for page in iter_pages()
]
