import os

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from apps.resources.views import dashboard_view
from apps.resources.views import analytics_dashboard_view
from apps.resources.views import big4_view
from apps.resources.views import topic_view

from apps.resources.views import (
    home_screen_view,
    success_view,
    dashboard_view,
    analytics_dashboard_view,
    resources_view,

    download_resource_view,
    


    # sandar
    directed_numbers_view,
    four_basic_operations_view,
    all_operations_view,
    koshuu_1_digit_view,
    big4_view,

    # onduktar
    onedigitarithmetics_view,
)

from apps.account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    activation_view,
    subscribe_request_view,
    RateLimitedPasswordResetView,
)

# Configurable so the real path never has to live in source control (same
# reasoning as SECRET_KEY) - set ADMIN_URL_PATH on the host to something
# private. Automated credential-stuffing bots scan the literal "admin/"
# path on every host they find, so a non-default path is a cheap layer of
# defense - not a substitute for real auth, but it stops the noise.
ADMIN_URL_PATH = os.environ.get('ADMIN_URL_PATH', 'admin/').strip('/') + '/'

urlpatterns = [
    path(ADMIN_URL_PATH, admin.site.urls),
    path('', home_screen_view, name='home'),
    path('home/', home_screen_view, name='home'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activation_view, name='activate'),
    path('account/', account_view, name='account'),
    path('subscribe/', subscribe_request_view, name='subscribe_request'),
    # Success message
    path('registration-success/', success_view, name='registration_success'),

    #sandar
    path('four_basic_operations/', four_basic_operations_view, name='four_basic_operations'),
    path('directed_numbers/', directed_numbers_view, name='directed_numbers'),
    path('all_operations/', all_operations_view, name='all_operations'),
    path('koshuu-1-digit/', koshuu_1_digit_view, name='koshuu_1_digit'),
    path('templates/interactive/big4/', big4_view, name='big4'),

    # for dynamic resources
    path(
        "topic/<slug:topic_slug>/<slug:subtopic_slug>/",
        topic_view,
        name="topic_page",
    ),

    path('resources/', include('apps.resources.urls')),

    #onduktar
    path('onedigitarithmetics/', onedigitarithmetics_view, name='onedigitarithmetics'),

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    path('analytics/', analytics_dashboard_view, name='analytics_dashboard'),

    # Resources
    path('resources/download/<int:pk>/', download_resource_view, name='download_resource'),
    path('resources/', resources_view, name='resources'),

    # Password management
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/', RateLimitedPasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html', subject_template_name='registration/password_reset_subject.txt'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)