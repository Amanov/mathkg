import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from apps.resources.views import home_screen_view
from config.media_views import public_media

# Configurable so the real path never has to live in source control (same
# reasoning as SECRET_KEY) - set ADMIN_URL_PATH on the host to something
# private. Automated credential-stuffing bots scan the literal "admin/"
# path on every host they find, so a non-default path is a cheap layer of
# defense - not a substitute for real auth, but it stops the noise.
ADMIN_URL_PATH = os.environ.get('ADMIN_URL_PATH', 'admin/').strip('/') + '/'

urlpatterns = [
    path(ADMIN_URL_PATH, admin.site.urls),
    # `/` and `/home/` both render the home page. `home` stays on
    # `/home/` because that is the path reverse() already returned
    # when the name was registered twice. Templates keep generating
    # the same href. `/` is home_root.
    path('', home_screen_view, name='home_root'),
    path('home/', home_screen_view, name='home'),
    path('', include('apps.account.urls')),
    path('', include('apps.resources.urlconf.core')),
    path('', include('apps.resources.urlconf.numbers')),
    path('', include('apps.resources.urlconf.algebra')),
    path('', include('apps.resources.urlconf.functions')),
    path('', include('apps.resources.urlconf.geometry')),
    path('', include('apps.resources.urlconf.data')),
    path('', include('apps.resources.urlconf.probability')),
    path('', include('apps.resources.urlconf.pages')),
    path('', include('apps.account.password_urls')),
]

if settings.DEBUG:
    # WhiteNoise serves collected static files in production. Development
    # still needs this helper for /static/.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Same allowlist in development and production. The old DEBUG static()
# helper, and the production catch-all, both published every file under
# MEDIA_ROOT — including resources/files/, which skipped the download view.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', public_media),
]
