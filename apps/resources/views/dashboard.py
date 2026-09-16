from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from apps.resources.models import Resource


@staff_member_required(login_url='login')
def dashboard_view(request):

    resources = Resource.objects.all()

    context = {
        'total_resources': resources.count(),
        'active_resources': resources.filter(is_active=True).count(),
        'total_downloads': resources.aggregate(
            Sum('download_count')
        )['download_count__sum'] or 0,

        'presentations': resources.filter(category='presentation'),
        'worksheets': resources.filter(category='worksheet'),
        'activities': resources.filter(category='activity'),
    }

    return render(
        request,
        'resources/dashboard.html',
        context
    )