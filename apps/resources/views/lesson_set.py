from django.shortcuts import render
from django.urls import reverse

from apps.resources.data.statistics_lesson_set import CARDS, IMAGE, SECTION_ORDER
from apps.resources.utils.resource_helpers import get_active_resources


def _links(files, resources, user):
    register_url = reverse('register')
    links = []
    for label, name in files:
        resource = resources.get(name)
        if resource is None:
            continue
        if user.is_authenticated:
            url = reverse('download_resource', kwargs={'pk': resource.id})
        else:
            url = register_url
        links.append({'label': label, 'url': url})
    return links


def statistics_lesson_view(request):
    """Mean, median, mode and range on one page, in the lesson-set layout."""
    resources = get_active_resources()
    grouped = {title: [] for title in SECTION_ORDER}
    for section, title, note, image, files in CARDS:
        grouped[section].append({
            'title': title,
            'note': note,
            'image': IMAGE + image,
            'links': _links(files, resources, request.user),
        })
    page = {
        'title': 'Орточо, медиана, мода, кулач',
        'grade_badge': '6–7 кл.',
        'lead': (
            '45 мүнөттүк сабак: тактадагы суроолор, иш барактары жооптору менен, '
            'иш-аракеттер жана мугалимге материалдар.'
        ),
        'sections': [
            {'title': title, 'cards': cards}
            for title, cards in grouped.items()
            if cards
        ],
    }
    return render(request, 'resources/lesson_set.html', {'page': page})
