from logging import getLogger

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.urls import reverse
from django.utils import timezone

from apps.resources.free_download import is_free_resource
from apps.resources.models import (
    Resource,
    ResourceDownload
)
from apps.resources.utils.request_helpers import get_client_ip

logger = getLogger(__name__)


def download_resource_view(request, pk):
    # Look the file up before the login check so the one free file on a
    # topic page can be downloaded with no account. A missing id still
    # sends a logged-out visitor to login, the same as before.
    resource = Resource.objects.filter(pk=pk, is_active=True).first()
    free = bool(resource and is_free_resource(resource.id))

    if not free:
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url=reverse('login'))

        resource = get_object_or_404(
            Resource,
            pk=pk,
            is_active=True
        )

        if not request.user.has_active_subscription:
            messages.error(
                request,
                'Сиздин жазылууңуздун мөөнөтү бүткөн. Уланта берүү үчүн жазылууну жаңыртыңыз.'
            )
            return redirect('account')

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
        user=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get(
            'HTTP_USER_AGENT',
            ''
        )[:500]
    )

    resource.increment_download()

    return FileResponse(file_handle, as_attachment=True)