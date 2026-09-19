from .models import SiteVisit

# Paths that shouldn't count as a "site visit" - staff tooling, static/media
# files (WhiteNoise usually serves these before Django even sees them, but
# excluded here too in case that ever changes), and the analytics page
# itself, which would otherwise inflate its own numbers every time someone
# checks it.
EXCLUDED_PREFIXES = ('/admin/', '/analytics/', '/static/', '/media/')


def get_client_ip(request):
    # Same Railway-proxy assumption as apps.account.views.get_client_ip -
    # REMOTE_ADDR is Railway's edge IP, not the visitor's.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class SiteVisitMiddleware:
    """Logs one row per qualifying page view, used to report total site
    traffic and unique visitors (distinct session_key) on the analytics
    dashboard. Staff members are excluded so the site owner's own admin
    browsing doesn't skew real audience numbers."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.method == 'GET'
            and response.status_code < 400
            and not request.path.startswith(EXCLUDED_PREFIXES)
            and not (request.user.is_authenticated and request.user.is_staff)
        ):
            if not request.session.session_key:
                request.session.save()
            SiteVisit.objects.create(
                session_key=request.session.session_key or '',
                user=request.user if request.user.is_authenticated else None,
                ip_address=get_client_ip(request),
                path=request.path[:255],
            )

        return response
