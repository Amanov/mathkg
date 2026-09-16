from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
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