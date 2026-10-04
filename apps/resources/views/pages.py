from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch

from ..models import MenuItem, NewsPost, Resource


def news_list_view(request):
    posts = NewsPost.objects.all()
    return render(request, 'resources/news_list.html', {'posts': posts})


def about_view(request):
    return render(request, 'resources/about.html')


def topics_tree_view(request):
    """The full menu hierarchy as one navigable page, for a visitor who
    wants to see/search the whole curriculum at once rather than click
    through the header menu level by level."""
    roots = MenuItem.objects.filter(parent__isnull=True).prefetch_related(
        'children',
        'children__children',
        'children__children__children',
        'children__children__children__children',
        'children__children__children__children__children',
    ).order_by('order')
    return render(request, 'resources/topics_tree.html', {'roots': roots})


def _menu_item_resolved_url(item):
    """A MenuItem's real page, or None if it's a pure category node (no
    Topic/Subtopic/Sub-subtopic pick and no resolvable url_name) - those
    don't have a page of their own, so a search result can't link to one."""
    resolved = item.get_resolved_url()
    if resolved:
        return resolved
    if item.url_name:
        try:
            return reverse(item.url_name)
        except NoReverseMatch:
            return None
    return None


def _menu_item_breadcrumb(item):
    """Ancestor titles from the root down to (not including) `item`."""
    titles = []
    ancestor = item.parent
    while ancestor is not None:
        titles.append(ancestor.title)
        ancestor = ancestor.parent
    titles.reverse()
    return titles


def _resource_resolved_url(resource):
    """The topic/subtopic/sub-subtopic page a Resource actually appears
    on - most specific pick first, same precedence as MenuItem's own."""
    try:
        if resource.subsubtopic_id:
            return reverse('subsubtopic_detail', args=[
                resource.topic.slug, resource.subtopic.slug, resource.subsubtopic.slug,
            ])
        if resource.subtopic_id:
            return reverse('subtopic_detail', args=[resource.topic.slug, resource.subtopic.slug])
        if resource.topic_id:
            return reverse('topic_detail', args=[resource.topic.slug])
    except NoReverseMatch:
        return None
    return None


def _topic_search_results(query_lower, limit):
    """Menu entries (and the "Темалар" bucket of the full results page use
    the same matching) whose title contains the query, most specific first
    by title, deduped by (title, url) since the same page can be reachable
    through more than one menu node.

    Matching is done in Python, not via a SQL icontains filter: SQLite's
    (and, depending on locale, Postgres's) case-insensitive LIKE only
    case-folds ASCII, so a lowercase Cyrillic query would silently miss
    every title stored with a capital letter. Python's str.lower() folds
    Cyrillic correctly, and this table is small enough (low thousands of
    rows) that filtering it in Python per request is cheap.
    """
    menu_matches = [
        item for item in MenuItem.objects.select_related(
            'parent', 'topic', 'subtopic', 'subsubtopic'
        )
        if query_lower in item.title.lower()
    ]
    menu_matches.sort(key=lambda item: item.title)

    results = []
    seen = set()
    for item in menu_matches:
        url = _menu_item_resolved_url(item)
        if not url or (item.title, url) in seen:
            continue
        seen.add((item.title, url))
        results.append({
            'title': item.title,
            'url': url,
            'breadcrumb': _menu_item_breadcrumb(item),
        })
        if len(results) >= limit:
            break
    return results


def _grouped_topic_results(results):
    """Group flat topic matches by their top-level menu category (Сандар,
    Пропорция, ...), in the same order as the main nav / /topics/ page,
    so the full results page reads as a page of topics - sectioned by
    category - rather than one undifferentiated list."""
    root_order = {
        item.title: item.order
        for item in MenuItem.objects.filter(parent__isnull=True)
    }
    groups = {}
    for result in results:
        category = result['breadcrumb'][0] if result['breadcrumb'] else 'Башка'
        groups.setdefault(category, []).append(result)
    return sorted(groups.items(), key=lambda pair: root_order.get(pair[0], 9999))


def search_suggest_view(request):
    """Backs the live dropdown under the header search box: as the visitor
    types, this returns a short list of matching topic pages as JSON so the
    page itself never reloads. The full /search/ page (below) still does
    the complete, all-content-types search for when they submit the form."""
    query = request.GET.get('q', '').strip()
    query_lower = query.lower()

    results = _topic_search_results(query_lower, limit=8) if len(query_lower) >= 2 else []

    return JsonResponse({
        'query': query,
        'results': results,
    })


def search_view(request):
    """Site-wide search: the topic menu and the resource library (title
    and description) - the content a visitor is actually looking for when
    they search for a topic. The news feed is a changelog, not curriculum
    content, so it's deliberately left out of search."""
    query = request.GET.get('q', '').strip()
    query_lower = query.lower()

    grouped_topic_results = []
    resource_results = []

    if query:
        topic_results = _topic_search_results(query_lower, limit=300)
        grouped_topic_results = _grouped_topic_results(topic_results)

        resource_matches = [
            resource for resource in Resource.objects.filter(
                is_active=True
            ).select_related('topic', 'subtopic', 'subsubtopic')
            if query_lower in resource.title.lower()
            or query_lower in resource.description.lower()
        ]
        resource_matches.sort(key=lambda resource: resource.title)

        for resource in resource_matches[:40]:
            resource_results.append({
                'resource': resource,
                'url': _resource_resolved_url(resource),
            })

    context = {
        'query': query,
        'grouped_topic_results': grouped_topic_results,
        'resource_results': resource_results,
        'has_results': bool(grouped_topic_results or resource_results),
    }
    return render(request, 'resources/search_results.html', context)
