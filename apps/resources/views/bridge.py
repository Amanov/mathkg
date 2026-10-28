from django.http import Http404
from django.shortcuts import render

from apps.resources.bridge_pages import CPA_LABELS, load_page, page_spec
from apps.resources.continuum import continuum_for_href
from apps.resources.topic_pages import build_topic_page
from apps.resources.utils.resource_helpers import get_active_resources


def bridge_topic_view(request, slug):
    data = load_page(slug)
    if data is None:
        raise Http404(slug)
    page = build_topic_page(page_spec(data), get_active_resources(), request.user)
    guide = data.get('bloom_guide') or []
    if guide:
        page['bloom_guide'] = [tuple(pair) for pair in guide]
    page['singapore'] = list(data.get('singapore') or [])
    cpa_rows = [
        item.get('cpa') or []
        for section in data.get('sections') or []
        for item in section.get('items') or []
    ]
    built = [item for section in page['sections'] for item in section['items']]
    for item, cpa in zip(built, cpa_rows):
        if cpa:
            item['cpa'] = [
                {'label': label, 'on': label in cpa}
                for label in CPA_LABELS
            ]
    nav = continuum_for_href(f'/{slug}/')
    if nav and nav.get('grade_band'):
        page['grade_badge'] = nav['grade_band']
    # Continuum cards used to sit under the title. The nine menu leaves
    # already have a prev/next above the footer, so the cards are not
    # drawn. «Маселе чыгаруу ыкмалары» is not a menu row; related_topics
    # uses this nav for that one footer link.
    return render(request, 'resources/bridge_topic.html', {
        'page': page,
        'topic_continuum': nav,
    })
