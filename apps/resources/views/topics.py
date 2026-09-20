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


def subtopic_detail(request, topic_slug, subtopic_slug):
    topic = get_object_or_404(Topic, slug=topic_slug)
    subtopic = get_object_or_404(Subtopic, slug=subtopic_slug, topic=topic)
    sections = build_topic_sections(subtopic)
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
    return render(request, 'resources/topic_page.html', {
        'topic': topic,
        'subtopic': subtopic,
        'subsubtopic': subsubtopic,
        'sections': sections,
    })
