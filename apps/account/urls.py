"""Sign-up, login, account, and the registration success page."""

from django.urls import path

from apps.resources.views import (
    success_view,
)

from apps.account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    activation_view,
    resend_activation_view,
    subscribe_request_view,
)

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activation_view, name='activate'),
    path('activate/resend/', resend_activation_view, name='resend_activation'),
    path('account/', account_view, name='account'),
    path('subscribe/', subscribe_request_view, name='subscribe_request'),
    # Success message
    path('registration-success/', success_view, name='registration_success'),
]
