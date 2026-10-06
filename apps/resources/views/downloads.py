from logging import getLogger

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.utils import timezone

from apps.resources.models import (
    Resource,
    ResourceDownload
)
from apps.resources.utils.request_helpers import get_client_ip

logger = getLogger(__name__)


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

    # Opened before logging the download or counting it against the daily
    # quota - a file missing from disk (the resource library isn't on
    # persistent storage yet - see docs/deployment-notes.md) must not
    # silently use up a slot or get counted as a successful download the
    # user never actually received.
    try:
        file_handle = resource.file.open('rb')
    except (FileNotFoundError, OSError):
        logger.error('Resource file missing on disk: resource_id=%s, file=%s', resource.pk, resource.file.name)
        messages.error(
            request,
            'Бул файл учурда жеткиликсиз. Бир аздан кийин кайра аракет '
            'кылыңыз же бизге жазыңыз: mathematicskgz@gmail.com'
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

    return FileResponse(file_handle, as_attachment=True)