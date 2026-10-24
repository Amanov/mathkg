from django.http import Http404
from django.shortcuts import render

from apps.resources.bridge_pages import load_page, page_spec
from apps.resources.topic_pages import build_topic_page
from apps.resources.utils.resource_helpers import get_active_resources


def bridge_topic_view(request, slug):
    data = load_page(slug)
    if data is None:
        raise Http404(slug)
    page = build_topic_page(page_spec(data), get_active_resources(), request.user)
    return render(request, 'resources/topic_materials.html', {'page': page})
