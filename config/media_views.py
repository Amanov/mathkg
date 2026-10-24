"""Which uploaded files may be fetched from /media/.

Presentations, worksheets, and the other paid downloads live under
resources/files/ (older rows also used resources/ and downloads/).
Those bytes only leave through download_resource_view, which still
applies the login, subscription, daily-cap, and free-file rules.

Pages embed two kinds of upload directly: resource thumbnails
(resources/images/) and the subscribe-modal QR code (payment_qr/).
Anything else under MEDIA_ROOT is not a public URL.
"""

import posixpath

from django.conf import settings
from django.http import Http404
from django.views.static import serve

# Prefixes templates request via ImageField.url. Keep the trailing slash
# so a sibling such as resources/images-private/ does not match.
PUBLIC_MEDIA_PREFIXES = (
    'resources/images/',
    'payment_qr/',
)


def is_public_media_path(path):
    if not path or '\\' in path or path.startswith(('/', '\\')):
        return False
    normalized = posixpath.normpath(path)
    if (
        not normalized
        or normalized == '.'
        or normalized.startswith('../')
        or normalized == '..'
    ):
        return False
    return any(normalized.startswith(prefix) for prefix in PUBLIC_MEDIA_PREFIXES)


def public_media(request, path):
    if not is_public_media_path(path):
        raise Http404()
    normalized = posixpath.normpath(path)
    return serve(request, normalized, document_root=settings.MEDIA_ROOT)
