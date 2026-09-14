from django.shortcuts import get_object_or_404
from django.http import FileResponse

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


def download_resource_view(request, pk):

    resource = get_object_or_404(
        Resource,
        pk=pk,
        is_active=True
    )

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

    return FileResponse(
        resource.file.open('rb'),
        as_attachment=True
    )