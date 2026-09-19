import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.resources.middleware import get_client_ip
from apps.resources.models import ButtonClick

# navigator.sendBeacon() can't attach Django's CSRF header, and the payload
# is just a label + path (nothing that mutates account state), so this one
# endpoint is deliberately exempt - same trade-off analytics beacons always
# make. Kept strict about method and payload size to limit abuse.
MAX_LABEL_LENGTH = 120
MAX_BODY_BYTES = 2048


@csrf_exempt
@require_POST
def track_click_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return HttpResponse(status=204)

    if len(request.body) > MAX_BODY_BYTES:
        return HttpResponse(status=400)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        label = str(payload.get('label', '')).strip()[:MAX_LABEL_LENGTH]
        path = str(payload.get('path', '')).strip()[:255]
    except (ValueError, UnicodeDecodeError):
        return HttpResponse(status=400)

    if not label:
        return HttpResponse(status=400)

    if not request.session.session_key:
        request.session.save()

    ButtonClick.objects.create(
        label=label,
        path=path,
        session_key=request.session.session_key or '',
        user=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
    )

    return HttpResponse(status=204)
