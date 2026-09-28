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

    # Сандар > Эквиваленттүүлүк (top-level topic) > Бөлчөктөрдү айландыруу -
    # all 10 slots, none with a real page yet.
    path('fractions-to-decimals/', operation_placeholder_view, {'operation_slug': 'fractions-to-decimals'}, name='fractions_to_decimals'),
    path('fractions-to-decimals-calculator/', operation_placeholder_view, {'operation_slug': 'fractions-to-decimals-calculator'}, name='fractions_to_decimals_calculator'),
    path('fractions-to-percentages/', operation_placeholder_view, {'operation_slug': 'fractions-to-percentages'}, name='fractions_to_percentages'),
    path('fractions-to-percentages-calculator/', operation_placeholder_view, {'operation_slug': 'fractions-to-percentages-calculator'}, name='fractions_to_percentages_calculator'),
    path('fractions-to-ratios/', operation_placeholder_view, {'operation_slug': 'fractions-to-ratios'}, name='fractions_to_ratios'),
    path('fractions-to-all/', operation_placeholder_view, {'operation_slug': 'fractions-to-all'}, name='fractions_to_all'),
    path('fractions-with-decimals/', operation_placeholder_view, {'operation_slug': 'fractions-with-decimals'}, name='fractions_with_decimals'),
    path('fractions-with-percentages/', operation_placeholder_view, {'operation_slug': 'fractions-with-percentages'}, name='fractions_with_percentages'),
    path('fractions-with-ratios/', operation_placeholder_view, {'operation_slug': 'fractions-with-ratios'}, name='fractions_with_ratios'),
    path('fractions-with-all/', operation_placeholder_view, {'operation_slug': 'fractions-with-all'}, name='fractions_with_all'),

    # Сандар > Эквиваленттүүлүк (top-level topic) > Ондуктарды айландыруу -
    # all 7 slots, none with a real page yet.
    path('decimals-to-fractions/', operation_placeholder_view, {'operation_slug': 'decimals-to-fractions'}, name='decimals_to_fractions'),
    path('decimals-to-percentages/', operation_placeholder_view, {'operation_slug': 'decimals-to-percentages'}, name='decimals_to_percentages'),
    path('decimals-to-both/', operation_placeholder_view, {'operation_slug': 'decimals-to-both'}, name='decimals_to_both'),
    path('decimals-recurring-to-fractions/', operation_placeholder_view, {'operation_slug': 'decimals-recurring-to-fractions'}, name='decimals_recurring_to_fractions'),
    path('decimals-with-fractions/', operation_placeholder_view, {'operation_slug': 'decimals-with-fractions'}, name='decimals_with_fractions'),
    path('decimals-with-percentages/', operation_placeholder_view, {'operation_slug': 'decimals-with-percentages'}, name='decimals_with_percentages'),
    path('decimals-with-both/', operation_placeholder_view, {'operation_slug': 'decimals-with-both'}, name='decimals_with_both'),

    # Сандар > Эквиваленттүүлүк (top-level topic) > Пайыздарды айландыруу -
    # all 8 slots, none with a real page yet.
    path('percentages-to-fractions/', operation_placeholder_view, {'operation_slug': 'percentages-to-fractions'}, name='percentages_to_fractions'),
    path('percentages-to-decimals/', operation_placeholder_view, {'operation_slug': 'percentages-to-decimals'}, name='percentages_to_decimals'),
    path('percentages-to-ratios/', operation_placeholder_view, {'operation_slug': 'percentages-to-ratios'}, name='percentages_to_ratios'),
    path('percentages-to-all/', operation_placeholder_view, {'operation_slug': 'percentages-to-all'}, name='percentages_to_all'),
    path('percentages-with-fractions/', operation_placeholder_view, {'operation_slug': 'percentages-with-fractions'}, name='percentages_with_fractions'),
    path('percentages-with-decimals/', operation_placeholder_view, {'operation_slug': 'percentages-with-decimals'}, name='percentages_with_decimals'),
    path('percentages-with-ratios/', operation_placeholder_view, {'operation_slug': 'percentages-with-ratios'}, name='percentages_with_ratios'),
    path('percentages-with-all/', operation_placeholder_view, {'operation_slug': 'percentages-with-all'}, name='percentages_with_all'),

    # Сандар > Эквиваленттүүлүк (top-level topic) > Катыштарды айландыруу -
    # all 6 slots, none with a real page yet.
    path('ratios-to-fractions/', operation_placeholder_view, {'operation_slug': 'ratios-to-fractions'}, name='ratios_to_fractions'),
    path('ratios-to-percentages/', operation_placeholder_view, {'operation_slug': 'ratios-to-percentages'}, name='ratios_to_percentages'),
    path('ratios-to-both/', operation_placeholder_view, {'operation_slug': 'ratios-to-both'}, name='ratios_to_both'),
    path('ratios-with-fractions/', operation_placeholder_view, {'operation_slug': 'ratios-with-fractions'}, name='ratios_with_fractions'),
    path('ratios-with-percentages/', operation_placeholder_view, {'operation_slug': 'ratios-with-percentages'}, name='ratios_with_percentages'),
    path('ratios-with-both/', operation_placeholder_view, {'operation_slug': 'ratios-with-both'}, name='ratios_with_both'),

    # Болжолдоо жана тегеректөө > Тегеректөө - all 4 slots, none with a
    # real page yet.
    path('rounding-decimal-places/', operation_placeholder_view, {'operation_slug': 'rounding-decimal-places'}, name='rounding_decimal_places'),
    path('rounding-significant-figures/', operation_placeholder_view, {'operation_slug': 'rounding-significant-figures'}, name='rounding_significant_figures'),
    path('rounding-mixed/', operation_placeholder_view, {'operation_slug': 'rounding-mixed'}, name='rounding_mixed'),
    path('rounding-whole-numbers/', operation_placeholder_view, {'operation_slug': 'rounding-whole-numbers'}, name='rounding_whole_numbers'),

    # Болжолдоо жана тегеректөө > Ката аралыктары - all 3 slots, none
    # with a real page yet.
    path('error-intervals-decimal-significant/', operation_placeholder_view, {'operation_slug': 'error-intervals-decimal-significant'}, name='error_intervals_decimal_significant'),
    path('error-intervals-calculations/', operation_placeholder_view, {'operation_slug': 'error-intervals-calculations'}, name='error_intervals_calculations'),
    path('error-intervals-truncation/', operation_placeholder_view, {'operation_slug': 'error-intervals-truncation'}, name='error_intervals_truncation'),

    # Бөлүүчүлөр, эселиктер жана жөнөкөй сандар > ЭЧОБ & ЭКОЭ: тизмелөө
    # менен - all 3 slots, none with a real page yet.
    path('hcf-listing/', operation_placeholder_view, {'operation_slug': 'hcf-listing'}, name='hcf_listing'),
    path('lcm-listing/', operation_placeholder_view, {'operation_slug': 'lcm-listing'}, name='lcm_listing'),
    path('hcf-lcm-listing-mixed/', operation_placeholder_view, {'operation_slug': 'hcf-lcm-listing-mixed'}, name='hcf_lcm_listing_mixed'),

    # Бөлүүчүлөр, эселиктер жана жөнөкөй сандар > ЭЧОБ & ЭКОЭ: жөнөкөй
    # көбөйтүүчүлөргө ажыратуу менен - all 3 slots, none with a real page yet.
    path('hcf-prime-factorisation/', operation_placeholder_view, {'operation_slug': 'hcf-prime-factorisation'}, name='hcf_prime_factorisation'),
    path('lcm-prime-factorisation/', operation_placeholder_view, {'operation_slug': 'lcm-prime-factorisation'}, name='lcm_prime_factorisation'),
    path('hcf-lcm-prime-factorisation-mixed/', operation_placeholder_view, {'operation_slug': 'hcf-lcm-prime-factorisation-mixed'}, name='hcf_lcm_prime_factorisation_mixed'),

    # Бөлчөктөр > Эсептөөлөр: бирдик бөлчөктөр - all 8 slots, none with a
    # real page yet.
    path('unit-fractions-adding/', operation_placeholder_view, {'operation_slug': 'unit-fractions-adding'}, name='unit_fractions_adding'),
    path('unit-fractions-subtracting/', operation_placeholder_view, {'operation_slug': 'unit-fractions-subtracting'}, name='unit_fractions_subtracting'),
    path('unit-fractions-adding-subtracting/', operation_placeholder_view, {'operation_slug': 'unit-fractions-adding-subtracting'}, name='unit_fractions_adding_subtracting'),
    path('unit-fractions-multiplying/', operation_placeholder_view, {'operation_slug': 'unit-fractions-multiplying'}, name='unit_fractions_multiplying'),
    path('unit-fractions-dividing/', operation_placeholder_view, {'operation_slug': 'unit-fractions-dividing'}, name='unit_fractions_dividing'),
    path('unit-fractions-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'unit-fractions-multiplying-dividing'}, name='unit_fractions_multiplying_dividing'),
    path('unit-fractions-with-integers/', operation_placeholder_view, {'operation_slug': 'unit-fractions-with-integers'}, name='unit_fractions_with_integers'),
    path('unit-fractions-mixed/', operation_placeholder_view, {'operation_slug': 'unit-fractions-mixed'}, name='unit_fractions_mixed'),

    # Бөлчөктөр > Эсептөөлөр: бирдик эмес бөлчөктөр - all 9 slots, none
    # with a real page yet.
    path('non-unit-fractions-adding/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-adding'}, name='non_unit_fractions_adding'),
    path('non-unit-fractions-subtracting/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-subtracting'}, name='non_unit_fractions_subtracting'),
    path('non-unit-fractions-adding-subtracting/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-adding-subtracting'}, name='non_unit_fractions_adding_subtracting'),
    path('non-unit-fractions-multiplying/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-multiplying'}, name='non_unit_fractions_multiplying'),
    path('non-unit-fractions-dividing/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-dividing'}, name='non_unit_fractions_dividing'),
    path('non-unit-fractions-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-multiplying-dividing'}, name='non_unit_fractions_multiplying_dividing'),
    path('non-unit-fractions-with-cancelling/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-with-cancelling'}, name='non_unit_fractions_with_cancelling'),
    path('non-unit-fractions-with-integers/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-with-integers'}, name='non_unit_fractions_with_integers'),
    path('non-unit-fractions-mixed/', operation_placeholder_view, {'operation_slug': 'non-unit-fractions-mixed'}, name='non_unit_fractions_mixed'),

    # Бөлчөктөр > Эквиваленттүүлүк - all 13 slots, none with a real page yet.
    path('fractions-equiv-to-decimals/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-to-decimals'}, name='fractions_equiv_to_decimals'),
    path('fractions-equiv-to-decimals-calculator/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-to-decimals-calculator'}, name='fractions_equiv_to_decimals_calculator'),
    path('fractions-equiv-to-percentages/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-to-percentages'}, name='fractions_equiv_to_percentages'),
    path('fractions-equiv-to-percentages-calculator/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-to-percentages-calculator'}, name='fractions_equiv_to_percentages_calculator'),
    path('fractions-equiv-to-ratios/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-to-ratios'}, name='fractions_equiv_to_ratios'),
    path('fractions-equiv-to-all/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-to-all'}, name='fractions_equiv_to_all'),
    path('fractions-equiv-with-decimals/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-with-decimals'}, name='fractions_equiv_with_decimals'),
    path('fractions-equiv-with-percentages/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-with-percentages'}, name='fractions_equiv_with_percentages'),
    path('fractions-equiv-with-ratios/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-with-ratios'}, name='fractions_equiv_with_ratios'),
    path('fractions-equiv-fdp/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-fdp'}, name='fractions_equiv_fdp'),
    path('fractions-equiv-fdp-ordering/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-fdp-ordering'}, name='fractions_equiv_fdp_ordering'),
    path('fractions-equiv-fpr/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-fpr'}, name='fractions_equiv_fpr'),
    path('fractions-equiv-fdpr/', operation_placeholder_view, {'operation_slug': 'fractions-equiv-fdpr'}, name='fractions_equiv_fdpr'),

    # Бөлчөктөр > Барабар бөлчөктөр - all 4 slots, none with a real page yet.
    path('equivalent-fractions-simplifying/', operation_placeholder_view, {'operation_slug': 'equivalent-fractions-simplifying'}, name='equivalent_fractions_simplifying'),
    path('equivalent-fractions-comparing-ordering/', operation_placeholder_view, {'operation_slug': 'equivalent-fractions-comparing-ordering'}, name='equivalent_fractions_comparing_ordering'),
    path('equivalent-fractions-comparing-inequality/', operation_placeholder_view, {'operation_slug': 'equivalent-fractions-comparing-inequality'}, name='equivalent_fractions_comparing_inequality'),
    path('equivalent-fractions-with-calculations/', operation_placeholder_view, {'operation_slug': 'equivalent-fractions-with-calculations'}, name='equivalent_fractions_with_calculations'),

    # Бөлчөктөр > Туюнтуу - all 2 slots, none with a real page yet.
    path('expressing-quantity/', operation_placeholder_view, {'operation_slug': 'expressing-quantity'}, name='expressing_quantity'),
    path('expressing-change/', operation_placeholder_view, {'operation_slug': 'expressing-change'}, name='expressing_change'),

    # Даражалар жана тамырлар > Даражалар (Indices) - all 11 slots, none
    # with a real page yet.
    path('indices-introduction/', operation_placeholder_view, {'operation_slug': 'indices-introduction'}, name='indices_introduction'),
    path('indices-square-numbers/', operation_placeholder_view, {'operation_slug': 'indices-square-numbers'}, name='indices_square_numbers'),
    path('indices-cube-numbers/', operation_placeholder_view, {'operation_slug': 'indices-cube-numbers'}, name='indices_cube_numbers'),
    path('indices-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'indices-multiplying-dividing'}, name='indices_multiplying_dividing'),
    path('indices-negative/', operation_placeholder_view, {'operation_slug': 'indices-negative'}, name='indices_negative'),
    path('indices-fractional/', operation_placeholder_view, {'operation_slug': 'indices-fractional'}, name='indices_fractional'),
    path('indices-negative-fractional/', operation_placeholder_view, {'operation_slug': 'indices-negative-fractional'}, name='indices_negative_fractional'),
    path('indices-with-brackets/', operation_placeholder_view, {'operation_slug': 'indices-with-brackets'}, name='indices_with_brackets'),
    path('indices-mixed/', operation_placeholder_view, {'operation_slug': 'indices-mixed'}, name='indices_mixed'),
    path('indices-equations/', operation_placeholder_view, {'operation_slug': 'indices-equations'}, name='indices_equations'),
    path('indices-reciprocals/', operation_placeholder_view, {'operation_slug': 'indices-reciprocals'}, name='indices_reciprocals'),

    # Даражалар жана тамырлар > Тамырларды эсептөө (Evaluating Roots) -
    # all 3 slots, none with a real page yet.
    path('evaluating-roots-estimating/', operation_placeholder_view, {'operation_slug': 'evaluating-roots-estimating'}, name='evaluating_roots_estimating'),
    path('evaluating-roots-square/', operation_placeholder_view, {'operation_slug': 'evaluating-roots-square'}, name='evaluating_roots_square'),
    path('evaluating-roots-square-cube/', operation_placeholder_view, {'operation_slug': 'evaluating-roots-square-cube'}, name='evaluating_roots_square_cube'),

    # Даражалар жана тамырлар > Тамырлар менен эсептөөлөр (Surds) - all 8
    # slots, none with a real page yet.
    path('surds-simplifying/', operation_placeholder_view, {'operation_slug': 'surds-simplifying'}, name='surds_simplifying'),
    path('surds-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'surds-multiplying-dividing'}, name='surds_multiplying_dividing'),
    path('surds-adding-subtracting/', operation_placeholder_view, {'operation_slug': 'surds-adding-subtracting'}, name='surds_adding_subtracting'),
    path('surds-expanding-brackets/', operation_placeholder_view, {'operation_slug': 'surds-expanding-brackets'}, name='surds_expanding_brackets'),
    path('surds-rationalising-without-conjugates/', operation_placeholder_view, {'operation_slug': 'surds-rationalising-without-conjugates'}, name='surds_rationalising_without_conjugates'),
    path('surds-rationalising-denominators/', operation_placeholder_view, {'operation_slug': 'surds-rationalising-denominators'}, name='surds_rationalising_denominators'),
    path('surds-mixed/', operation_placeholder_view, {'operation_slug': 'surds-mixed'}, name='surds_mixed'),
    path('surds-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'surds-with-pythagoras'}, name='surds_with_pythagoras'),

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