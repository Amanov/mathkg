from datetime import timedelta

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.resources.models import (
    Resource,
    ResourceDownload,
    SiteVisit,
)


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
    # Context
    # =========================

    context = {
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
    }

    return render(
        request,
        'analytics/analytics_dashboard.html',
        context
    )