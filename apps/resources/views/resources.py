from django.shortcuts import render

from apps.resources.models import Resource


def resources_view(request):

    category = request.GET.get('category')

    resources = Resource.objects.filter(
        is_active=True
    )

    if category:
        resources = resources.filter(
            category=category
        )

    context = {
        'resources': resources,
        'categories': Resource.CATEGORY_CHOICES,
        'selected_category': category,
    }

    return render(
        request,
        'personal/resources.html',
        context
    )

    from django.shortcuts import render, get_object_or_404

from ..models import (
    Topic,
    Subtopic,
    Resource,
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

    resources = Resource.objects.filter(
        subtopic=subtopic,
        is_active=True
    )

    context = {
        "topic": topic,
        "subtopic": subtopic,
        "resources": resources,
    }

    return render(
        request,
        "resources/topic_page.html",
        context
    )