from urllib.parse import urlencode

from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch
from django_ratelimit.decorators import ratelimit

from apps.account.models import SubscriptionRequest, DAILY_DOWNLOAD_LIMITS
from apps.resources.grade_search import (
    catalog_index,
    grade_page_numbers,
    grade_counts,
    norm_url,
    pages_for_search,
    parse_grade_query,
    preview_results,
    section_sort_key,
)
from apps.resources.utils.request_helpers import get_client_ip

from ..models import MenuItem, NewsPost, Resource, SearchQuery

# Below this, a query is too unspecific to be worth running at all - every
# title/description in the catalog gets scanned in Python per request (see
# _topic_search_results's docstring for why that's not a DB-level
# icontains), so a 1-character or empty query is the cheapest way to make
# that scan run for nothing. search_suggest_view enforces the same floor.
MIN_SEARCH_QUERY_LENGTH = 2


def _search_ratelimit_key(group, request):
    return get_client_ip(request)


def menu_fragment_view(request):
    """The full topic menu, loaded after the first screen.

    The home page only sends the top row. This response is the same
    markup the menu used to inline, so opening it looks the same.
    It is cacheable and is not a page view.
    """
    from apps.resources.views.context_processors import root_menu

    response = render(request, 'partials/menu_fragment.html', {
        'menu_items': root_menu(full=True),
    })
    response['Cache-Control'] = 'public, max-age=3600'
    response['X-Robots-Tag'] = 'noindex'
    return response


def news_list_view(request):
    posts = NewsPost.objects.all()
    return render(request, 'resources/news_list.html', {'posts': posts})


def about_view(request):
    return render(request, 'resources/about.html')


def video_guide_view(request):
    return render(request, 'resources/video_guide.html')


def pricing_view(request):
    plan_names = {
        SubscriptionRequest.PLAN_THREE_MONTHS: '3 ай',
        SubscriptionRequest.PLAN_SIX_MONTHS: '6 ай',
        SubscriptionRequest.PLAN_ONE_YEAR: '1 жыл',
    }
    unlimited_display = {'presentation': 'Чексиз', 'worksheet': 'Чексиз', 'activity': 'Чексиз'}
    plans = []
    for code, name in plan_names.items():
        limits = DAILY_DOWNLOAD_LIMITS[code]
        plans.append({
            'code': code,
            'name': name,
            'price_som': SubscriptionRequest.PLAN_PRICE_SOM[code],
            'months': SubscriptionRequest.PLAN_MONTHS[code],
            'limits': limits or unlimited_display,
        })
    return render(request, 'resources/pricing.html', {
        'plans': plans,
        'featured_code': SubscriptionRequest.PLAN_ONE_YEAR,
    })


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
    """Group flat topic matches by their top-level section (Сандар,
    Пропорция, Алгебра, Геометрия, Дата, Ыктымалдуулук), then any other
    menu root, so the page reads as topics sectioned by category."""
    root_order = {
        item.title: item.order
        for item in MenuItem.objects.filter(parent__isnull=True)
    }
    groups = {}
    for result in results:
        category = result['breadcrumb'][0] if result['breadcrumb'] else 'Башка'
        groups.setdefault(category, []).append(result)
    return sorted(
        groups.items(),
        key=lambda pair: section_sort_key(pair[0], root_order),
    )


def _attach_grades(results):
    index = catalog_index()
    for result in results:
        page = index.get(norm_url(result['url']))
        if page:
            result['grade'] = page['label']
    return results


def _topic_results_for(text, grade):
    """Topic pages for a text query, or for a class named in the query."""
    if grade is None:
        if len(text) < MIN_SEARCH_QUERY_LENGTH:
            return []
        return _attach_grades(_topic_search_results(text, limit=300))

    results = pages_for_search(grade, text)
    if not text:
        return results

    seen = {row['url'] for row in results}
    index = catalog_index()
    for row in _topic_search_results(text.lower(), limit=300):
        url = norm_url(row['url'])
        if url in seen:
            continue
        page = index.get(url)
        if page and grade in page['grades']:
            row['url'] = url
            row['grade'] = page['label']
            results.append(row)
            seen.add(url)
    results.sort(key=lambda row: (
        section_sort_key(row['breadcrumb'][0] if row['breadcrumb'] else ''),
        row['title'],
    ))
    return results


def _search_grade(query, explicit):
    """The class to filter by, the words besides that class, and whether
    the class was written in the search box (so a chip can rewrite it)."""
    grade_from_text, remainder = parse_grade_query(query)
    grade = grade_from_text
    if explicit.isdigit():
        number = int(explicit)
        if 1 <= number <= 12:
            grade = number
    text = remainder if grade_from_text else query
    if len(text) < MIN_SEARCH_QUERY_LENGTH:
        text = ''
    return grade, text, grade_from_text, remainder


def _grade_chips(query, text, grade, grade_from_text, remainder):
    counts = grade_counts(text)
    if len(counts) < 2:
        return [], ''
    base = reverse('search')

    def href(params):
        return base + ('?' + urlencode(params) if params else '')

    chips = []
    for number in sorted(counts):
        if grade_from_text or not query:
            chip_query = f'{number}-класс'
            if remainder:
                chip_query = f'{chip_query} {remainder}'
            link = href({'q': chip_query})
        else:
            link = href({'q': query, 'grade': number})
        chips.append({
            'num': number,
            'label': f'{number}-класс',
            'count': counts[number],
            'href': link,
        })
    if grade_from_text:
        clear_params = {'q': remainder} if remainder else {}
    else:
        clear_params = {'q': query} if query else {}
    return chips, href(clear_params)


def grade_page_view(request, grade):
    """Every topic page of one class, grouped by section.

    A plain list page for search engines and for a teacher who types
    "4 класс математика". It is linked from the footer, not the menu.
    """
    grades = grade_page_numbers()
    if grade not in grades:
        raise Http404('No such class')
    grouped = _grouped_topic_results(pages_for_search(grade, ''))
    return render(request, 'resources/grade_page.html', {
        'grade': grade,
        'grades': grades,
        'grouped_topic_results': grouped,
        'topic_count': sum(len(rows) for _section, rows in grouped),
    })


@ratelimit(key=_search_ratelimit_key, rate='30/m', method='GET', block=True)
def search_suggest_view(request):
    """Backs the live dropdown under the header search box: as the visitor
    types, this returns a short list of matching topic pages as JSON so the
    page itself never reloads. The full /search/ page (below) still does
    the complete, all-content-types search for when they submit the form."""
    query = request.GET.get('q', '').strip()
    grade, text, _from_text, _remainder = _search_grade(query, '')

    if grade is not None:
        results = preview_results(_topic_results_for(text, grade), limit=8)
    elif len(query) >= MIN_SEARCH_QUERY_LENGTH:
        results = _topic_results_for(query.lower(), None)[:8]
    else:
        results = []

    return JsonResponse({
        'query': query,
        'results': results,
    })


@ratelimit(key=_search_ratelimit_key, rate='30/m', method='GET', block=True)
def search_view(request):
    """Site-wide search: the topic menu and the resource library (title
    and description) - the content a visitor is actually looking for when
    they search for a topic. The news feed is a changelog, not curriculum
    content, so it's deliberately left out of search."""
    query = request.GET.get('q', '').strip()
    query_lower = query.lower()
    grade, text, grade_from_text, remainder = _search_grade(
        query, request.GET.get('grade', '').strip(),
    )

    grouped_topic_results = []
    resource_results = []
    grade_chips = []
    grade_clear_href = ''

    if grade is not None or len(query_lower) >= MIN_SEARCH_QUERY_LENGTH:
        topic_text = text if grade is not None else query_lower
        topic_results = _topic_results_for(topic_text, grade)
        grouped_topic_results = _grouped_topic_results(topic_results)

        resource_matches = []
        # A pure class query ("7-класс") has no words to match against a
        # file title. Resource rows also have no class of their own, so a
        # class filter keeps only files that sit on a matching topic page.
        if len(text if grade is not None else query_lower) >= MIN_SEARCH_QUERY_LENGTH:
            needle = (text if grade is not None else query_lower).lower()
            resource_matches = [
                resource for resource in Resource.objects.filter(
                    is_active=True
                ).select_related('topic', 'subtopic', 'subsubtopic')
                if needle in resource.title.lower()
                or needle in resource.description.lower()
            ]
            if grade is not None:
                index = catalog_index()
                kept = []
                for resource in resource_matches:
                    page = index.get(norm_url(_resource_resolved_url(resource) or ''))
                    if page and grade in page['grades']:
                        kept.append(resource)
                resource_matches = kept
            resource_matches.sort(key=lambda resource: resource.title)

        for resource in resource_matches[:40]:
            resource_results.append({
                'resource': resource,
                'url': _resource_resolved_url(resource),
            })

        grade_chips, grade_clear_href = _grade_chips(
            query, text, grade, grade_from_text, remainder,
        )

        # Logged only for a submitted search (not search_suggest_view's
        # per-keystroke dropdown, which would flood this table with
        # partial, non-deliberate queries).
        if not request.session.session_key:
            request.session.save()
        SearchQuery.objects.create(
            query=query or f'{grade}-класс',
            results_count=len(topic_results) + len(resource_matches),
            session_key=request.session.session_key or '',
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
        )

    context = {
        'query': query,
        'grouped_topic_results': grouped_topic_results,
        'resource_results': resource_results,
        'has_results': bool(grouped_topic_results or resource_results),
        'grade_chips': grade_chips,
        'active_grade': grade,
        'grade_clear_href': grade_clear_href,
    }
    return render(request, 'resources/search_results.html', context)
