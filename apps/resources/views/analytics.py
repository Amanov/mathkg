from datetime import datetime, time, timedelta

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Max, Q, Value
from django.db.models.functions import Coalesce, TruncDate
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.resources.models import (
    AnalyticsWindow,
    KYRGYZ_MONTHS,
    Resource,
    ResourceDownload,
    SiteVisit,
    ButtonClick,
    SearchQuery,
    LoginEvent,
    PageReaction,
    PageReactionCount,
)

# Thresholds for the "policy watch" panel - flags patterns worth a human
# look, not proof of a violation on their own. Tuned for a small Kyrgyz
# teacher-resource site: a real teacher rarely downloads from more than a
# couple of devices/networks in a day, and rarely needs dozens of
# worksheets in one sitting, so both point at likely account sharing or
# scripted bulk-downloading rather than normal use.
SHARED_IP_WINDOW_HOURS = 24
SHARED_IP_THRESHOLD = 3
BULK_DOWNLOAD_WINDOW_HOURS = 24
BULK_DOWNLOAD_THRESHOLD = 30
SAME_FILE_MULTI_IP_THRESHOLD = 2
SHARED_IP_LOGIN_WINDOW_DAYS = 7
SHARED_IP_LOGIN_THRESHOLD = 3

# A "session" (for time-on-site) is a run of page views from the same
# browser with no gap longer than this - the standard web-analytics
# definition (GA/Matomo etc. default to 30 min too), since a session
# cookie can otherwise live for weeks and make "time on site" meaningless.
SESSION_GAP_MINUTES = 30
SESSION_WINDOW_DAYS = 30


def format_stats_since(since):
    """Kyrgyz banner instant, in the active timezone.

    «Статистика 4-ноябрь 2026, 11:00 баштап эсептелүүдө»
    """
    local = timezone.localtime(since)
    month = KYRGYZ_MONTHS[local.month - 1]
    return (
        f'Статистика {local.day}-{month} {local.year}, '
        f'{local:%H:%M} баштап эсептелүүдө'
    )


def parse_since_param(raw):
    """Temporary ?since=YYYY-MM-DD view, as local midnight. Invalid values are ignored."""
    if not raw:
        return None
    try:
        day = datetime.strptime(str(raw).strip(), '%Y-%m-%d').date()
    except ValueError:
        return None
    midnight = datetime.combine(day, time.min)
    return timezone.make_aware(midnight, timezone.get_current_timezone())


def resolve_dashboard_since(request):
    """Effective cutoff, whether this request is only previewing it, and the date-input value.

    A valid ?since= date overrides the stored cutoff for this response
    and is not written. The stored value is what the reset buttons change.
    """
    stored = AnalyticsWindow.stored_since()
    raw = str(request.GET.get('since') or '').strip()
    temporary = parse_since_param(raw)
    if temporary is not None:
        return temporary, True, raw
    return stored, False, ''


def _start_of_day(day):
    midnight = datetime.combine(day, time.min)
    return timezone.make_aware(midnight, timezone.get_current_timezone())


def _apply_since(qs, field, since):
    if since is None:
        return qs
    return qs.filter(**{f'{field}__gte': since})


def _apply_window(qs, field, window_start, since):
    """Start a 7-day or 30-day window at max(window start, since).

    Date windows keep the original __date lookup when the cutoff is not
    later than that window, so an all-time dashboard matches the
    previous counts. A cutoff part-way through the window uses a
    datetime bound so earlier rows on that calendar day stay out.
    """
    if isinstance(window_start, datetime):
        start = window_start
        if timezone.is_naive(start):
            start = timezone.make_aware(start, timezone.get_current_timezone())
        if since is not None and since > start:
            start = since
        return qs.filter(**{f'{field}__gte': start})

    if since is not None and since > _start_of_day(window_start):
        return qs.filter(**{f'{field}__gte': since})
    return qs.filter(**{f'{field}__date__gte': window_start})


def _download_count(since):
    if since is None:
        return Count('downloads')
    return Count('downloads', filter=Q(downloads__downloaded_at__gte=since))


def _reaction_summary(since):
    """Face totals, then the pages with the most happy and sad faces.

    With no cutoff, the ranked lists stay on PageReactionCount (the
    all-time admin totals). With a cutoff, both the totals and the
    ranked lists are counted from PageReaction rows in the window.
    """
    if since is None:
        faces_qs = PageReaction.objects.all()
        top_happy = list(
            PageReactionCount.objects.filter(happy_count__gt=0)
            .order_by('-happy_count', 'path')[:8]
        )
        top_sad = list(
            PageReactionCount.objects.filter(sad_count__gt=0)
            .order_by('-sad_count', 'path')[:8]
        )
    else:
        faces_qs = PageReaction.objects.filter(created_at__gte=since)
        top_happy = list(
            faces_qs.filter(face=PageReaction.FACE_HAPPY)
            .values('path')
            .annotate(happy_count=Count('id'), material=Max('material'))
            .order_by('-happy_count', 'path')[:8]
        )
        top_sad = list(
            faces_qs.filter(face=PageReaction.FACE_SAD)
            .values('path')
            .annotate(sad_count=Count('id'), material=Max('material'))
            .order_by('-sad_count', 'path')[:8]
        )
    faces = {
        row['face']: row['total']
        for row in faces_qs.values('face').annotate(total=Count('id'))
    }
    return faces, top_happy, top_sad


@staff_member_required(login_url='login')
@require_http_methods(['GET', 'HEAD', 'POST'])
def analytics_dashboard_view(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return HttpResponseForbidden('Бул аракет суперколдонуучуга гана.')
        action = request.POST.get('action')
        if action == 'since_now':
            # timezone.now() is an absolute instant. The banner renders
            # it in TIME_ZONE (Asia/Bishkek).
            AnalyticsWindow.set_since(timezone.now())
        elif action == 'clear':
            AnalyticsWindow.set_since(None)
        return redirect('analytics_dashboard')

    since, stats_since_temporary, stats_since_input = resolve_dashboard_since(request)

    # Calendar day in Asia/Bishkek. timezone.now().date() is the UTC day,
    # which is still yesterday here from 00:00–06:00.
    today = timezone.localdate()

    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    thirty_days_ago = today - timedelta(days=29)

    # =========================
    # Overall Statistics
    # =========================

    total_resources = Resource.objects.filter(
        is_active=True
    ).count()

    total_downloads = _apply_since(
        ResourceDownload.objects, 'downloaded_at', since
    ).count()

    unique_users = (
        _apply_since(ResourceDownload.objects, 'downloaded_at', since)
        .filter(user__isnull=False)
        .values('user')
        .distinct()
        .count()
    )

    # =========================
    # Site Traffic (page views logged by SiteVisitMiddleware)
    # =========================

    total_visits = _apply_since(SiteVisit.objects, 'visited_at', since).count()

    unique_visitors = (
        _apply_since(SiteVisit.objects, 'visited_at', since)
        .values('session_key')
        .distinct()
        .count()
    )

    visits_this_week = _apply_window(
        SiteVisit.objects, 'visited_at', week_ago, since
    ).count()

    unique_visitors_this_week = (
        _apply_window(SiteVisit.objects, 'visited_at', week_ago, since)
        .values('session_key')
        .distinct()
        .count()
    )

    visits_this_month = _apply_window(
        SiteVisit.objects, 'visited_at', month_ago, since
    ).count()

    unique_visitors_this_month = (
        _apply_window(SiteVisit.objects, 'visited_at', month_ago, since)
        .values('session_key')
        .distinct()
        .count()
    )

    top_pages = (
        _apply_since(SiteVisit.objects, 'visited_at', since)
        .values('path')
        .annotate(views=Count('id'))
        .order_by('-views')[:10]
    )

    visit_counts_by_day = {}
    visitor_counts_by_day = {}
    for row in (
        _apply_window(SiteVisit.objects, 'visited_at', thirty_days_ago, since)
        .annotate(day=TruncDate('visited_at'))
        .values('day')
        .annotate(
            views=Count('id'),
            visitors=Count('session_key', distinct=True),
        )
    ):
        visit_counts_by_day[row['day']] = row['views']
        visitor_counts_by_day[row['day']] = row['visitors']

    daily_visit_stats = [
        {
            'date': the_date.strftime('%m/%d'),
            'views': visit_counts_by_day.get(the_date, 0),
            'visitors': visitor_counts_by_day.get(the_date, 0),
        }
        for the_date in (thirty_days_ago + timedelta(days=i) for i in range(30))
    ]

    # =========================
    # Returning vs New Visitors
    # =========================
    # A "returning visitor" is a session that shows up on 2+ distinct
    # calendar days - a session's cookie only tells us it's the same
    # browser, not that they came back on purpose, but visiting again on
    # a different day is the clearest signal of that we can get without
    # requiring login.

    sessions_by_day_count = (
        _apply_since(SiteVisit.objects, 'visited_at', since)
        .values('session_key')
        .annotate(days_active=Count('visited_at__date', distinct=True))
    )
    total_sessions_tracked = sessions_by_day_count.count()
    returning_visitors = sessions_by_day_count.filter(days_active__gte=2).count()
    new_visitors = total_sessions_tracked - returning_visitors
    returning_visitor_pct = (
        round(returning_visitors / total_sessions_tracked * 100, 1)
        if total_sessions_tracked else 0
    )

    # =========================
    # Time on Site
    # =========================
    # SiteVisit only logs a timestamp per page view, so "time on site" has
    # to be reconstructed: group each session's page views (within the
    # last SESSION_WINDOW_DAYS) in order, and split them into separate
    # visits wherever the gap between two views exceeds SESSION_GAP_MINUTES.
    # A session with only one page view in a burst has no measurable
    # duration - it's counted toward the bounce rate instead of averaged in.

    session_window_start = timezone.now() - timedelta(days=SESSION_WINDOW_DAYS)
    gap = timedelta(minutes=SESSION_GAP_MINUTES)

    session_burst_durations = []
    single_page_bursts = 0
    burst_start = burst_last = None
    current_session_key = None

    recent_visits = (
        _apply_window(SiteVisit.objects, 'visited_at', session_window_start, since)
        .order_by('session_key', 'visited_at')
        .values_list('session_key', 'visited_at')
    )
    for session_key, visited_at in recent_visits:
        if session_key != current_session_key or (visited_at - burst_last) > gap:
            if burst_start is not None:
                if burst_start == burst_last:
                    single_page_bursts += 1
                else:
                    session_burst_durations.append((burst_last - burst_start).total_seconds() / 60)
            current_session_key = session_key
            burst_start = visited_at
        burst_last = visited_at
    if burst_start is not None:
        if burst_start == burst_last:
            single_page_bursts += 1
        else:
            session_burst_durations.append((burst_last - burst_start).total_seconds() / 60)

    engaged_sessions = len(session_burst_durations)
    total_bursts = engaged_sessions + single_page_bursts
    avg_session_minutes = (
        round(sum(session_burst_durations) / engaged_sessions, 1)
        if engaged_sessions else 0
    )
    bounce_rate_pct = (
        round(single_page_bursts / total_bursts * 100, 1)
        if total_bursts else 0
    )

    # =========================
    # Logins
    # =========================

    total_logins = _apply_since(LoginEvent.objects, 'logged_in_at', since).count()

    logins_this_week = _apply_window(
        LoginEvent.objects, 'logged_in_at', week_ago, since
    ).count()
    logins_this_month = _apply_window(
        LoginEvent.objects, 'logged_in_at', month_ago, since
    ).count()

    login_counts_by_day = {
        row['day']: row['count']
        for row in (
            _apply_window(LoginEvent.objects, 'logged_in_at', thirty_days_ago, since)
            .annotate(day=TruncDate('logged_in_at'))
            .values('day')
            .annotate(count=Count('id'))
        )
    }

    daily_login_stats = [
        login_counts_by_day.get(the_date, 0)
        for the_date in (thirty_days_ago + timedelta(days=i) for i in range(30))
    ]

    top_login_users = (
        _apply_since(LoginEvent.objects, 'logged_in_at', since)
        .values('user__username', 'user__email')
        .annotate(login_count=Count('id'))
        .order_by('-login_count')[:10]
    )

    # =========================
    # Most Clicked Buttons
    # =========================

    total_clicks = _apply_since(ButtonClick.objects, 'clicked_at', since).count()

    top_buttons = (
        _apply_since(ButtonClick.objects, 'clicked_at', since)
        .values('label')
        .annotate(clicks=Count('id'))
        .order_by('-clicks')[:15]
    )

    # =========================
    # Search Queries
    # =========================

    total_searches = _apply_since(SearchQuery.objects, 'searched_at', since).count()

    top_queries = (
        _apply_since(SearchQuery.objects, 'searched_at', since)
        .values('query')
        .annotate(searches=Count('id'))
        .order_by('-searches')[:15]
    )

    # Queries that came back empty, most-repeated first - a direct signal
    # of content gaps (what teachers are looking for but the site doesn't
    # have yet), not just a usage stat.
    zero_result_queries = (
        _apply_since(SearchQuery.objects, 'searched_at', since)
        .filter(results_count=0)
        .values('query')
        .annotate(searches=Count('id'))
        .order_by('-searches')[:15]
    )

    # =========================
    # Policy Watch - possible ToS violations
    # =========================

    # Rolling windows from an aware instant, not a calendar date, so a
    # "24 hours" or "7 days" cutoff is the same length in Bishkek as in UTC.
    shared_ip_cutoff = timezone.now() - timedelta(hours=SHARED_IP_WINDOW_HOURS)

    flagged_shared_ip_accounts = (
        ResourceDownload.objects
        .filter(user__isnull=False, downloaded_at__gte=shared_ip_cutoff)
        .exclude(ip_address__isnull=True)
        .values('user__id', 'user__username', 'user__email')
        .annotate(
            distinct_ips=Count('ip_address', distinct=True),
            dl_count=Count('id'),
        )
        .filter(distinct_ips__gte=SHARED_IP_THRESHOLD)
        .order_by('-distinct_ips')
    )

    bulk_download_cutoff = timezone.now() - timedelta(hours=BULK_DOWNLOAD_WINDOW_HOURS)

    flagged_bulk_download_accounts = (
        ResourceDownload.objects
        .filter(user__isnull=False, downloaded_at__gte=bulk_download_cutoff)
        .values('user__id', 'user__username', 'user__email')
        .annotate(dl_count=Count('id'))
        .filter(dl_count__gte=BULK_DOWNLOAD_THRESHOLD)
        .order_by('-dl_count')
    )

    # Same user + same file, downloaded from 2+ distinct IPs - a much more
    # direct account-sharing signal than "downloaded from several IPs that
    # day" (a teacher legitimately switching between home wifi and a phone
    # hotspot for DIFFERENT files isn't suspicious; needing the exact same
    # worksheet again from a brand-new IP usually means someone else has
    # the login). All-time, not windowed, since a second household using
    # the account for the same file two weeks apart is still sharing.
    flagged_same_file_multi_ip = (
        ResourceDownload.objects
        .filter(user__isnull=False)
        .exclude(ip_address__isnull=True)
        .values('user__id', 'user__username', 'user__email', 'resource__id', 'resource__title')
        .annotate(
            distinct_ips=Count('ip_address', distinct=True),
            dl_count=Count('id'),
        )
        .filter(distinct_ips__gte=SAME_FILE_MULTI_IP_THRESHOLD)
        .order_by('-distinct_ips', '-dl_count')
    )

    def with_admin_link(rows):
        rows = list(rows)
        for row in rows:
            row['admin_url'] = reverse('admin:account_account_change', args=[row['user__id']])
        return rows

    login_ip_cutoff = timezone.now() - timedelta(days=SHARED_IP_LOGIN_WINDOW_DAYS)

    flagged_shared_ip_logins = (
        LoginEvent.objects
        .filter(logged_in_at__gte=login_ip_cutoff)
        .exclude(ip_address__isnull=True)
        .values('user__id', 'user__username', 'user__email')
        .annotate(
            distinct_ips=Count('ip_address', distinct=True),
            login_count=Count('id'),
        )
        .filter(distinct_ips__gte=SHARED_IP_LOGIN_THRESHOLD)
        .order_by('-distinct_ips')
    )

    def with_admin_link(rows):
        rows = list(rows)
        for row in rows:
            row['admin_url'] = reverse('admin:account_account_change', args=[row['user__id']])
        return rows

    flagged_shared_ip_accounts = with_admin_link(flagged_shared_ip_accounts)
    flagged_bulk_download_accounts = with_admin_link(flagged_bulk_download_accounts)
    flagged_same_file_multi_ip = with_admin_link(flagged_same_file_multi_ip)
    flagged_shared_ip_logins = with_admin_link(flagged_shared_ip_logins)
    total_flagged_accounts = (
        len(flagged_shared_ip_accounts)
        + len(flagged_bulk_download_accounts)
        + len(flagged_same_file_multi_ip)
        + len(flagged_shared_ip_logins)
    )

    # =========================
    # Downloads
    # =========================

    downloads_this_week = _apply_window(
        ResourceDownload.objects, 'downloaded_at', week_ago, since
    ).count()

    downloads_this_month = _apply_window(
        ResourceDownload.objects, 'downloaded_at', month_ago, since
    ).count()

    # =========================
    # Top Downloaded Resources
    # =========================

    top_resources = (
        Resource.objects
        .annotate(
            dl_count=_download_count(since)
        )
        .order_by('-dl_count')[:10]
    )

    # =========================
    # Top Users
    # =========================

    top_users = (
        _apply_since(ResourceDownload.objects, 'downloaded_at', since)
        .filter(user__isnull=False)
        .values(
            'user__username',
            'user__email'
        )
        .annotate(
            download_count=Count('id')
        )
        .order_by('-download_count')[:10]
    )

    # =========================
    # Category Statistics
    # =========================

    category_stats = (
        Resource.objects
        .values('category')
        .annotate(
            total_downloads=_download_count(since)
        )
        .order_by('-total_downloads')
    )

    # =========================
    # Downloads by Folder (Topic)
    # =========================

    downloads_by_folder = (
        _apply_since(ResourceDownload.objects, 'downloaded_at', since)
        .annotate(folder=Coalesce('resource__topic__title', Value('Башка')))
        .values('folder')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # =========================
    # Recent Downloads
    # =========================

    recent_downloads = (
        _apply_since(ResourceDownload.objects, 'downloaded_at', since)
        .select_related(
            'resource',
            'user'
        )
        .order_by('-downloaded_at')[:20]
    )

    # =========================
    # Daily Download Trend
    # =========================

    counts_by_day = {
        row['day']: row['count']
        for row in (
            _apply_window(
                ResourceDownload.objects, 'downloaded_at', thirty_days_ago, since
            )
            .annotate(day=TruncDate('downloaded_at'))
            .values('day')
            .annotate(count=Count('id'))
        )
    }

    daily_stats = [
        {
            'date': date.strftime('%m/%d'),
            'count': counts_by_day.get(date, 0),
        }
        for date in (thirty_days_ago + timedelta(days=i) for i in range(30))
    ]

    # =========================
    # Chart data (fed to json_script in the template - Chart.js reads these)
    # =========================

    # "View data" table twins for each chart - every value a chart shows
    # must also be reachable without hovering it.
    traffic_table_rows = list(reversed([
        {
            'date': v['date'],
            'visits': v['views'],
            'visitors': v['visitors'],
            'logins': daily_login_stats[i],
        }
        for i, v in enumerate(daily_visit_stats)
    ]))
    download_table_rows = list(reversed(daily_stats))

    chart_traffic_labels = [d['date'] for d in daily_visit_stats]
    chart_traffic_visits = [d['views'] for d in daily_visit_stats]
    chart_traffic_visitors = [d['visitors'] for d in daily_visit_stats]
    chart_traffic_logins = daily_login_stats
    chart_download_labels = [d['date'] for d in daily_stats]
    chart_download_counts = [d['count'] for d in daily_stats]
    chart_button_labels = [b['label'] for b in top_buttons]
    chart_button_counts = [b['clicks'] for b in top_buttons]
    chart_folder_labels = [d['folder'] for d in downloads_by_folder]
    chart_folder_counts = [d['total'] for d in downloads_by_folder]
    chart_query_labels = [q['query'] for q in top_queries]
    chart_query_counts = [q['searches'] for q in top_queries]

    reaction_faces, reaction_top_happy, reaction_top_sad = _reaction_summary(since)

    # =========================
    # Context
    # =========================

    context = {
        # renders this page with the standard Django admin chrome (user
        # tools, sidebar, breadcrumbs) since the template extends
        # admin/base_site.html rather than the public site's base.html
        **admin.site.each_context(request),
        'title': 'Analytics Dashboard',

        'total_resources': total_resources,
        'total_downloads': total_downloads,
        'unique_users': unique_users,
        'downloads_this_week': downloads_this_week,
        'downloads_this_month': downloads_this_month,
        'top_resources': top_resources,
        'top_users': top_users,
        'category_stats': category_stats,
        'recent_downloads': recent_downloads,
        'daily_stats': daily_stats,
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'visits_this_week': visits_this_week,
        'unique_visitors_this_week': unique_visitors_this_week,
        'visits_this_month': visits_this_month,
        'unique_visitors_this_month': unique_visitors_this_month,
        'top_pages': top_pages,
        'daily_visit_stats': daily_visit_stats,
        'total_clicks': total_clicks,
        'top_buttons': top_buttons,
        'total_searches': total_searches,
        'top_queries': top_queries,
        'zero_result_queries': zero_result_queries,
        'flagged_shared_ip_accounts': flagged_shared_ip_accounts,
        'flagged_bulk_download_accounts': flagged_bulk_download_accounts,
        'flagged_same_file_multi_ip': flagged_same_file_multi_ip,
        'flagged_shared_ip_logins': flagged_shared_ip_logins,
        'total_flagged_accounts': total_flagged_accounts,
        'shared_ip_window_hours': SHARED_IP_WINDOW_HOURS,
        'shared_ip_threshold': SHARED_IP_THRESHOLD,
        'bulk_download_window_hours': BULK_DOWNLOAD_WINDOW_HOURS,
        'bulk_download_threshold': BULK_DOWNLOAD_THRESHOLD,
        'shared_ip_login_window_days': SHARED_IP_LOGIN_WINDOW_DAYS,

        # returning / new visitors
        'total_sessions_tracked': total_sessions_tracked,
        'returning_visitors': returning_visitors,
        'new_visitors': new_visitors,
        'returning_visitor_pct': returning_visitor_pct,

        # time on site
        'avg_session_minutes': avg_session_minutes,
        'engaged_sessions': engaged_sessions,
        'bounce_rate_pct': bounce_rate_pct,

        # logins
        'total_logins': total_logins,
        'logins_this_week': logins_this_week,
        'logins_this_month': logins_this_month,
        'top_login_users': top_login_users,

        # downloads by folder
        'downloads_by_folder': downloads_by_folder,

        # table-view twins
        'traffic_table_rows': traffic_table_rows,
        'download_table_rows': download_table_rows,

        # chart payloads
        'chart_traffic_labels': chart_traffic_labels,
        'chart_traffic_visits': chart_traffic_visits,
        'chart_traffic_visitors': chart_traffic_visitors,
        'chart_traffic_logins': chart_traffic_logins,
        'chart_download_labels': chart_download_labels,
        'chart_download_counts': chart_download_counts,
        'chart_button_labels': chart_button_labels,
        'chart_button_counts': chart_button_counts,
        'chart_folder_labels': chart_folder_labels,
        'chart_folder_counts': chart_folder_counts,
        'chart_query_labels': chart_query_labels,
        'chart_query_counts': chart_query_counts,

        'reaction_happy': reaction_faces.get(PageReaction.FACE_HAPPY, 0),
        'reaction_ok': reaction_faces.get(PageReaction.FACE_OK, 0),
        'reaction_sad': reaction_faces.get(PageReaction.FACE_SAD, 0),
        'reaction_top_happy': reaction_top_happy,
        'reaction_top_sad': reaction_top_sad,

        'stats_limited': since is not None,
        'stats_since_banner': format_stats_since(since) if since else '',
        'stats_since_temporary': stats_since_temporary,
        'stats_since_input': stats_since_input,
    }

    return render(
        request,
        'analytics/analytics_dashboard.html',
        context
    )