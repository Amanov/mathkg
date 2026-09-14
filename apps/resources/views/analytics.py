from datetime import timedelta

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone

from apps.resources.models import (
    Resource,
    ResourceDownload
)


@staff_member_required
def analytics_dashboard_view(request):

    today = timezone.now().date()

    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

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

    daily_stats = []

    for i in range(30):

        date = today - timedelta(days=i)

        count = (
            ResourceDownload.objects
            .filter(downloaded_at__date=date)
            .count()
        )

        daily_stats.append({
            'date': date.strftime('%m/%d'),
            'count': count,
        })

    daily_stats.reverse()

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
    }

    return render(
        request,
        'analytics/analytics_dashboard.html',
        context
    )