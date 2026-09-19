from datetime import timedelta

from django.shortcuts import render
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Value
from django.db.models.functions import Coalesce, TruncDate
from django.urls import reverse
from django.utils import timezone

from apps.resources.models import (
    Resource,
    ResourceDownload,
    SiteVisit,
    ButtonClick,
    LoginEvent,
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


@staff_member_required(login_url='login')
def analytics_dashboard_view(request):

    today = timezone.now().date()

    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    thirty_days_ago = today - timedelta(days=29)

    # =========================
    # Overall Statistics
    # =========================

    total_resources = Resource.objects.filter(
        is_active=True
    ).count()

    total_downloads = ResourceDownload.objects.count()

    unique_users = (
        ResourceDownload.objects
        .filter(user__isnull=False)
        .values('user')
        .distinct()
        .count()
    )

    # =========================
    # Site Traffic (page views logged by SiteVisitMiddleware)
    # =========================

    total_visits = SiteVisit.objects.count()

    unique_visitors = (
        SiteVisit.objects
        .values('session_key')
        .distinct()
        .count()
    )

    visits_this_week = (
        SiteVisit.objects
        .filter(visited_at__date__gte=week_ago)
        .count()
    )

    unique_visitors_this_week = (
        SiteVisit.objects
        .filter(visited_at__date__gte=week_ago)
        .values('session_key')
        .distinct()
        .count()
    )

    visits_this_month = (
        SiteVisit.objects
        .filter(visited_at__date__gte=month_ago)
        .count()
    )

    unique_visitors_this_month = (
        SiteVisit.objects
        .filter(visited_at__date__gte=month_ago)
        .values('session_key')
        .distinct()
        .count()
    )

    top_pages = (
        SiteVisit.objects
        .values('path')
        .annotate(views=Count('id'))
        .order_by('-views')[:10]
    )

    visit_counts_by_day = {}
    visitor_counts_by_day = {}
    for row in (
        SiteVisit.objects
        .filter(visited_at__date__gte=thirty_days_ago)
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
        SiteVisit.objects
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
        SiteVisit.objects
        .filter(visited_at__gte=session_window_start)
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

    total_logins = LoginEvent.objects.count()

    logins_this_week = LoginEvent.objects.filter(logged_in_at__date__gte=week_ago).count()
    logins_this_month = LoginEvent.objects.filter(logged_in_at__date__gte=month_ago).count()

    login_counts_by_day = {
        row['day']: row['count']
        for row in (
            LoginEvent.objects
            .filter(logged_in_at__date__gte=thirty_days_ago)
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
        LoginEvent.objects
        .values('user__username', 'user__email')
        .annotate(login_count=Count('id'))
        .order_by('-login_count')[:10]
    )

    # =========================
    # Most Clicked Buttons
    # =========================

    total_clicks = ButtonClick.objects.count()

    top_buttons = (
        ButtonClick.objects
        .values('label')
        .annotate(clicks=Count('id'))
        .order_by('-clicks')[:15]
    )

    # =========================
    # Policy Watch - possible ToS violations
    # =========================

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

    downloads_this_week = (
        ResourceDownload.objects
        .filter(downloaded_at__date__gte=week_ago)
        .count()
    )

    downloads_this_month = (
        ResourceDownload.objects
        .filter(downloaded_at__date__gte=month_ago)
        .count()
    )

    # =========================
    # Top Downloaded Resources
    # =========================

    top_resources = (
        Resource.objects
        .annotate(
            dl_count=Count('downloads')
        )
        .order_by('-dl_count')[:10]
    )

    # =========================
    # Top Users
    # =========================

    top_users = (
        ResourceDownload.objects
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
            total_downloads=Count('downloads')
        )
        .order_by('-total_downloads')
    )

    # =========================
    # Downloads by Folder (Topic)
    # =========================

    downloads_by_folder = (
        ResourceDownload.objects
        .annotate(folder=Coalesce('resource__topic__title', Value('Башка')))
        .values('folder')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # =========================
    # Recent Downloads
    # =========================

    recent_downloads = (
        ResourceDownload.objects
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
            ResourceDownload.objects
            .filter(downloaded_at__date__gte=thirty_days_ago)
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
    }

    return render(
        request,
        'analytics/analytics_dashboard.html',
        context
    )