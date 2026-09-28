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
    track_click_view,
    


    # sandar
    directed_numbers_view,
    four_basic_operations_view,
    all_operations_view,
    koshuu_1_digit_view,
    big4_view,

    # onduktar
    onedigitarithmetics_view,
    operation_placeholder_view,

    # ekvivalenttuuluk
    to_fractions_view,
    to_percentages_view,
    to_both_view,
    recurring_decimals_to_fractions_view,
    with_fractions_view,
    with_percentages_view,
    fdp_view,
    fdp_ordering_view,
    fdpr_view,

    # pages
    news_list_view,
    about_view,
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

    # Ондуктар > Эсептөөлөр: 1 орундук сандар - the other 7 operation
    # slots (Кошуу/Adding is the one real page, koshuu-1-digit above).
    # Short flat URLs matching koshuu-1-digit/'s own convention, not the
    # long generic /resources/topic/number/... path.
    path('subtracting-1-digit/', operation_placeholder_view, {'operation_slug': 'subtracting-1-digit'}, name='subtracting_1_digit'),
    path('adding-subtracting-1-digit/', operation_placeholder_view, {'operation_slug': 'adding-subtracting-1-digit'}, name='adding_subtracting_1_digit'),
    path('multiplying-1-digit/', operation_placeholder_view, {'operation_slug': 'multiplying-1-digit'}, name='multiplying_1_digit'),
    path('dividing-1-digit/', operation_placeholder_view, {'operation_slug': 'dividing-1-digit'}, name='dividing_1_digit'),
    path('multiplying-dividing-1-digit/', operation_placeholder_view, {'operation_slug': 'multiplying-dividing-1-digit'}, name='multiplying_dividing_1_digit'),
    path('mixed-1-digit/', operation_placeholder_view, {'operation_slug': 'mixed-1-digit'}, name='mixed_1_digit'),
    path('dividing-by-less-than-1/', operation_placeholder_view, {'operation_slug': 'dividing-by-less-than-1'}, name='dividing_by_less_than_1'),

    # Ондуктар > Эсептөөлөр: 1 жана 2 орундук сандар - all 8 slots, none
    # with a real page yet.
    path('adding-1-2-digit/', operation_placeholder_view, {'operation_slug': 'adding-1-2-digit'}, name='adding_1_2_digit'),
    path('subtracting-1-2-digit/', operation_placeholder_view, {'operation_slug': 'subtracting-1-2-digit'}, name='subtracting_1_2_digit'),
    path('adding-subtracting-1-2-digit/', operation_placeholder_view, {'operation_slug': 'adding-subtracting-1-2-digit'}, name='adding_subtracting_1_2_digit'),
    path('multiplying-1-2-digit/', operation_placeholder_view, {'operation_slug': 'multiplying-1-2-digit'}, name='multiplying_1_2_digit'),
    path('dividing-1-2-digit/', operation_placeholder_view, {'operation_slug': 'dividing-1-2-digit'}, name='dividing_1_2_digit'),
    path('multiplying-dividing-1-2-digit/', operation_placeholder_view, {'operation_slug': 'multiplying-dividing-1-2-digit'}, name='multiplying_dividing_1_2_digit'),
    path('multiplying-dividing-10-100-1000/', operation_placeholder_view, {'operation_slug': 'multiplying-dividing-10-100-1000'}, name='multiplying_dividing_10_100_1000'),
    path('mixed-1-2-digit/', operation_placeholder_view, {'operation_slug': 'mixed-1-2-digit'}, name='mixed_1_2_digit'),

    # Ондуктар > Эсептөөлөр: бүтүн сандар менен - all 8 slots, none with a
    # real page yet.
    path('adding-with-integers/', operation_placeholder_view, {'operation_slug': 'adding-with-integers'}, name='adding_with_integers'),
    path('subtracting-with-integers/', operation_placeholder_view, {'operation_slug': 'subtracting-with-integers'}, name='subtracting_with_integers'),
    path('adding-subtracting-with-integers/', operation_placeholder_view, {'operation_slug': 'adding-subtracting-with-integers'}, name='adding_subtracting_with_integers'),
    path('multiplying-with-integers/', operation_placeholder_view, {'operation_slug': 'multiplying-with-integers'}, name='multiplying_with_integers'),
    path('dividing-with-integers/', operation_placeholder_view, {'operation_slug': 'dividing-with-integers'}, name='dividing_with_integers'),
    path('multiplying-dividing-with-integers/', operation_placeholder_view, {'operation_slug': 'multiplying-dividing-with-integers'}, name='multiplying_dividing_with_integers'),
    path('mixed-with-integers/', operation_placeholder_view, {'operation_slug': 'mixed-with-integers'}, name='mixed_with_integers'),
    path('dividing-divisor-less-than-1-with-integers/', operation_placeholder_view, {'operation_slug': 'dividing-divisor-less-than-1-with-integers'}, name='dividing_divisor_less_than_1_with_integers'),

    # Ондуктар > Эквиваленттүүлүк - 9 real, hand-built pages (unlike the
    # placeholder groups above), each rewired from the old dead
    # `download_file` scheme onto the current download_resource system.
    path('to-fractions/', to_fractions_view, name='to_fractions'),
    path('to-percentages/', to_percentages_view, name='to_percentages'),
    path('to-both/', to_both_view, name='to_both'),
    path('recurring-decimals-to-fractions/', recurring_decimals_to_fractions_view, name='recurring_decimals_to_fractions'),
    path('with-fractions/', with_fractions_view, name='with_fractions'),
    path('with-percentages/', with_percentages_view, name='with_percentages'),
    path('fdp/', fdp_view, name='fdp'),
    path('fdp-ordering/', fdp_ordering_view, name='fdp_ordering'),
    path('fdpr/', fdpr_view, name='fdpr'),

    # Ондуктар > Акча - all 5 slots, none with a real page yet.
    path('purchasing-calculator/', operation_placeholder_view, {'operation_slug': 'purchasing-calculator'}, name='purchasing_calculator'),
    path('purchasing-non-calculator/', operation_placeholder_view, {'operation_slug': 'purchasing-non-calculator'}, name='purchasing_non_calculator'),
    path('hire-purchase/', operation_placeholder_view, {'operation_slug': 'hire-purchase'}, name='hire_purchase'),
    path('bills-and-statements/', operation_placeholder_view, {'operation_slug': 'bills-and-statements'}, name='bills_and_statements'),
    path('rates-of-pay/', operation_placeholder_view, {'operation_slug': 'rates-of-pay'}, name='rates_of_pay'),

    # Ондуктар > Мезгилдүү ондуктар - both slots, neither with a real page yet.
    path('recurring-decimals-ordering/', operation_placeholder_view, {'operation_slug': 'recurring-decimals-ordering'}, name='recurring_decimals_ordering'),
    path('recurring-converting-to-fractions/', operation_placeholder_view, {'operation_slug': 'recurring-converting-to-fractions'}, name='recurring_converting_to_fractions'),

    # Багытталган сандар > Эсептөөлөр - all 7 slots, none with a real page yet.
    path('adding-directed/', operation_placeholder_view, {'operation_slug': 'adding-directed'}, name='adding_directed'),
    path('subtracting-directed/', operation_placeholder_view, {'operation_slug': 'subtracting-directed'}, name='subtracting_directed'),
    path('adding-subtracting-directed/', operation_placeholder_view, {'operation_slug': 'adding-subtracting-directed'}, name='adding_subtracting_directed'),
    path('multiplying-dividing-directed/', operation_placeholder_view, {'operation_slug': 'multiplying-dividing-directed'}, name='multiplying_dividing_directed'),
    path('mixed-directed/', operation_placeholder_view, {'operation_slug': 'mixed-directed'}, name='mixed_directed'),
    path('with-bidmas-directed/', operation_placeholder_view, {'operation_slug': 'with-bidmas-directed'}, name='with_bidmas_directed'),
    path('complex-directed/', operation_placeholder_view, {'operation_slug': 'complex-directed'}, name='complex_directed'),

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    path('analytics/', analytics_dashboard_view, name='analytics_dashboard'),
    path('track-click/', track_click_view, name='track_click'),

    # Resources
    path('resources/download/<int:pk>/', download_resource_view, name='download_resource'),
    path('resources/', resources_view, name='resources'),

    # Pages
    path('news/', news_list_view, name='news_list'),
    path('about/', about_view, name='about'),

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