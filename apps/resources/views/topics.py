from django.shortcuts import (
    render,
    get_object_or_404,
)

from ..models import (
    Topic,
    Subtopic,
)

from ..services import (
    build_topic_sections,
)


def topic_view(
    request,
    topic_slug,
    subtopic_slug
):

    topic = get_object_or_404(
        Topic,
        slug=topic_slug
    )

    subtopic = get_object_or_404(
        Subtopic,
        slug=subtopic_slug,
        topic=topic
    )

    sections = build_topic_sections(
        subtopic
    )

    return render(
        request,
        "resources/topic_page.html",
        {
            "topic": topic,
            "subtopic": subtopic,
            "sections": sections,
        }
    )

def topic_detail(request, topic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    subtopics = topic.subtopics.all()
    return render(request, 'resources/topic_detail.html', {
        'topic': topic,
        'subtopics': subtopics,
    })


def _pack_page(request, key, title, sections):
    """An empty database page that a grade pack teaches shows that pack in
    the topic layout (see data/pack_pages.py PATH_PAGES)."""
    if sections:
        return None
    from apps.resources.data.pack_pages import page_for
    from apps.resources.topic_pages import build_topic_page
    from apps.resources.utils.resource_helpers import get_active_resources
    spec = page_for(key, title)
    if spec is None:
        return None
    page = build_topic_page(spec, get_active_resources(), request.user)
    return render(request, 'resources/topic_materials.html', {'page': page})


def subtopic_detail(request, topic_slug, subtopic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    subtopic = get_object_or_404(Subtopic, slug=subtopic_slug, topic=topic)
    sections = build_topic_sections(subtopic)
    pack = _pack_page(request, (topic_slug, subtopic_slug), subtopic.title, sections)
    if pack:
        return pack
    return render(request, 'resources/topic_page.html', {
        'topic': topic,
        'subtopic': subtopic,
        'sections': sections,
    })


def subsubtopic_detail(request, topic_slug, subtopic_slug, subsubtopic_slug):
    from ..models import SubSubtopic
    topic = get_object_or_404(Topic, slug=topic_slug)
    subtopic = get_object_or_404(Subtopic, slug=subtopic_slug, topic=topic)
    subsubtopic = get_object_or_404(SubSubtopic, slug=subsubtopic_slug, subtopic=subtopic)
    sections = build_topic_sections(subtopic, subsubtopic)
    pack = _pack_page(request, (topic_slug, subtopic_slug, subsubtopic_slug), subsubtopic.title, sections)
    if pack:
        return pack
    return render(request, 'resources/topic_page.html', {
        'topic': topic,
        'subtopic': subtopic,
        'subsubtopic': subsubtopic,
        'sections': sections,
    })
