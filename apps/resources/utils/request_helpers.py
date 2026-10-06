def get_client_ip(request):
    """The visitor's real IP, used for rate-limit keys and download/login
    logging. Railway terminates TLS and proxies every request to this app,
    so REMOTE_ADDR is always Railway's edge IP, never the visitor's - the
    first X-Forwarded-For value is the real client IP as long as Railway
    stays the only hop in front of this app. If that ever changes (e.g. a
    CDN added in front of Railway), this needs a trusted-proxy-aware
    rewrite, since a client could otherwise spoof this header themselves.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
