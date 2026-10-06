from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.utils import timezone

from apps.resources.models import (
    Resource,
    ResourceDownload
)


def get_client_ip(request):

    x_forwarded_for = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


@login_required(login_url='login')
def download_resource_view(request, pk):

    if not request.user.has_active_subscription:
        messages.error(
            request,
            'Сиздин жазылууңуздун мөөнөтү бүткөн. Уланта берүү үчүн жазылууну жаңыртыңыз.'
        )
        return redirect('account')

    resource = get_object_or_404(
        Resource,
        pk=pk,
        is_active=True
    )

    # A resource already downloaded today never gets blocked by the daily
    # limit, even once that limit is used up - a retry or an accidental
    # double-click shouldn't cost the user the very file they just got.
    already_downloaded_today = ResourceDownload.objects.filter(
        user=request.user, resource=resource,
        downloaded_at__date=timezone.now().date(),
    ).exists()

    if not already_downloaded_today:
        remaining = request.user.downloads_remaining_today(resource.category)
        if remaining is not None and remaining <= 0:
            messages.error(
                request,
                f"Бүгүнкү «{resource.get_category_display()}» жүктөп алуу "
                "чегине жеттиңиз. Эртең кайра аракет кылыңыз же планыңызды "
                "жаңыртыңыз."
            )
            return redirect('account')

    ResourceDownload.objects.create(
        resource=resource,
        user=request.user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get(
            'HTTP_USER_AGENT',
            ''
        )[:500]
    )

    resource.increment_download()

    return FileResponse(
        resource.file.open('rb'),
        as_attachment=True
    )