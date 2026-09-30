import os

from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

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

    # question bank / online tests
    question_bank_view,
    question_create_view,
    exam_list_view,
    exam_create_view,
    exam_detail_view,
    exam_take_view,
    exam_submit_view,
    exam_result_view,
)

from apps.account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    activation_view,
    subscribe_request_view,
    school_dashboard_view,
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
    path('school/', school_dashboard_view, name='school_dashboard'),
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

    # Бүтүн сандар > Эсептөөлөр: 1 жана 2 орундук - all 8 slots, none
    # with a real page yet.
    path('integers-adding-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-adding-1-2-digit'}, name='integers_adding_1_2_digit'),
    path('integers-subtracting-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-subtracting-1-2-digit'}, name='integers_subtracting_1_2_digit'),
    path('integers-adding-subtracting-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-adding-subtracting-1-2-digit'}, name='integers_adding_subtracting_1_2_digit'),
    path('integers-multiplying-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-1-2-digit'}, name='integers_multiplying_1_2_digit'),
    path('integers-dividing-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-dividing-1-2-digit'}, name='integers_dividing_1_2_digit'),
    path('integers-multiplying-dividing-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-dividing-1-2-digit'}, name='integers_multiplying_dividing_1_2_digit'),
    path('integers-multiplying-dividing-10-100-1000/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-dividing-10-100-1000'}, name='integers_multiplying_dividing_10_100_1000'),
    path('integers-mixed-1-2-digit/', operation_placeholder_view, {'operation_slug': 'integers-mixed-1-2-digit'}, name='integers_mixed_1_2_digit'),

    # Бүтүн сандар > Эсептөөлөр: 2 жана 3 орундук - all 7 slots, none
    # with a real page yet.
    path('integers-adding-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-adding-2-3-digit'}, name='integers_adding_2_3_digit'),
    path('integers-subtracting-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-subtracting-2-3-digit'}, name='integers_subtracting_2_3_digit'),
    path('integers-adding-subtracting-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-adding-subtracting-2-3-digit'}, name='integers_adding_subtracting_2_3_digit'),
    path('integers-multiplying-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-2-3-digit'}, name='integers_multiplying_2_3_digit'),
    path('integers-dividing-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-dividing-2-3-digit'}, name='integers_dividing_2_3_digit'),
    path('integers-multiplying-dividing-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-dividing-2-3-digit'}, name='integers_multiplying_dividing_2_3_digit'),
    path('integers-mixed-2-3-digit/', operation_placeholder_view, {'operation_slug': 'integers-mixed-2-3-digit'}, name='integers_mixed_2_3_digit'),

    # Бүтүн сандар > Эсептөөлөр: ондуктар менен - all 8 slots, none with
    # a real page yet.
    path('integers-adding-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-adding-with-decimals'}, name='integers_adding_with_decimals'),
    path('integers-subtracting-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-subtracting-with-decimals'}, name='integers_subtracting_with_decimals'),
    path('integers-adding-subtracting-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-adding-subtracting-with-decimals'}, name='integers_adding_subtracting_with_decimals'),
    path('integers-multiplying-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-with-decimals'}, name='integers_multiplying_with_decimals'),
    path('integers-dividing-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-dividing-with-decimals'}, name='integers_dividing_with_decimals'),
    path('integers-multiplying-dividing-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-multiplying-dividing-with-decimals'}, name='integers_multiplying_dividing_with_decimals'),
    path('integers-mixed-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-mixed-with-decimals'}, name='integers_mixed_with_decimals'),
    path('integers-dividing-divisor-less-than-1-with-decimals/', operation_placeholder_view, {'operation_slug': 'integers-dividing-divisor-less-than-1-with-decimals'}, name='integers_dividing_divisor_less_than_1_with_decimals'),

    # Бүтүн сандар > Турмуштук маселелер - both slots, none with a real
    # page yet.
    path('integers-real-life-calculator/', operation_placeholder_view, {'operation_slug': 'integers-real-life-calculator'}, name='integers_real_life_calculator'),
    path('integers-real-life-non-calculator/', operation_placeholder_view, {'operation_slug': 'integers-real-life-non-calculator'}, name='integers_real_life_non_calculator'),

    # Өлчөмдөр > Татаал өлчөмдөр (Compound) - all 7 slots, none with a
    # real page yet.
    path('compound-area-volume-conversion/', operation_placeholder_view, {'operation_slug': 'compound-area-volume-conversion'}, name='compound_area_volume_conversion'),
    path('compound-density-mass-volume/', operation_placeholder_view, {'operation_slug': 'compound-density-mass-volume'}, name='compound_density_mass_volume'),
    path('compound-work-hours/', operation_placeholder_view, {'operation_slug': 'compound-work-hours'}, name='compound_work_hours'),
    path('compound-population-density/', operation_placeholder_view, {'operation_slug': 'compound-population-density'}, name='compound_population_density'),
    path('compound-pressure-force-area/', operation_placeholder_view, {'operation_slug': 'compound-pressure-force-area'}, name='compound_pressure_force_area'),
    path('compound-rates-of-pay/', operation_placeholder_view, {'operation_slug': 'compound-rates-of-pay'}, name='compound_rates_of_pay'),
    path('compound-speed-distance-time/', operation_placeholder_view, {'operation_slug': 'compound-speed-distance-time'}, name='compound_speed_distance_time'),

    # Өлчөмдөр > Акча - all 5 slots, none with a real page yet.
    path('measures-money-purchasing-calculator/', operation_placeholder_view, {'operation_slug': 'measures-money-purchasing-calculator'}, name='measures_money_purchasing_calculator'),
    path('measures-money-purchasing-non-calculator/', operation_placeholder_view, {'operation_slug': 'measures-money-purchasing-non-calculator'}, name='measures_money_purchasing_non_calculator'),
    path('measures-money-hire-purchase/', operation_placeholder_view, {'operation_slug': 'measures-money-hire-purchase'}, name='measures_money_hire_purchase'),
    path('measures-money-bills-statements/', operation_placeholder_view, {'operation_slug': 'measures-money-bills-statements'}, name='measures_money_bills_statements'),
    path('measures-money-rates-of-pay/', operation_placeholder_view, {'operation_slug': 'measures-money-rates-of-pay'}, name='measures_money_rates_of_pay'),

    # Өлчөмдөр > Масштабдуу сүрөттөр - all 4 slots, none with a real
    # page yet.
    path('scale-drawings-lengths/', operation_placeholder_view, {'operation_slug': 'scale-drawings-lengths'}, name='scale_drawings_lengths'),
    path('scale-drawings-estimation/', operation_placeholder_view, {'operation_slug': 'scale-drawings-estimation'}, name='scale_drawings_estimation'),
    path('scale-drawings-with-bearings/', operation_placeholder_view, {'operation_slug': 'scale-drawings-with-bearings'}, name='scale_drawings_with_bearings'),
    path('scale-drawings-areas/', operation_placeholder_view, {'operation_slug': 'scale-drawings-areas'}, name='scale_drawings_areas'),

    # Өлчөмдөр > Өлчөө системалары - all 4 slots, none with a real page
    # yet.
    path('systems-of-measurement-imperial/', operation_placeholder_view, {'operation_slug': 'systems-of-measurement-imperial'}, name='systems_of_measurement_imperial'),
    path('systems-of-measurement-metric/', operation_placeholder_view, {'operation_slug': 'systems-of-measurement-metric'}, name='systems_of_measurement_metric'),
    path('systems-of-measurement-mixed/', operation_placeholder_view, {'operation_slug': 'systems-of-measurement-mixed'}, name='systems_of_measurement_mixed'),
    path('systems-of-measurement-conversion-factors/', operation_placeholder_view, {'operation_slug': 'systems-of-measurement-conversion-factors'}, name='systems_of_measurement_conversion_factors'),

    # Өлчөмдөр > Аянт жана көлөм бирдиктерин алмаштыруу (top-level
    # sibling) - all 3 slots, none with a real page yet.
    path('area-volume-conversion-area/', operation_placeholder_view, {'operation_slug': 'area-volume-conversion-area'}, name='area_volume_conversion_area'),
    path('area-volume-conversion-volume/', operation_placeholder_view, {'operation_slug': 'area-volume-conversion-volume'}, name='area_volume_conversion_volume'),
    path('area-volume-conversion-mixed/', operation_placeholder_view, {'operation_slug': 'area-volume-conversion-mixed'}, name='area_volume_conversion_mixed'),

    # Өлчөмдөр > Убакыт (Time) - all 5 slots, none with a real page yet.
    path('time-reading-clocks/', operation_placeholder_view, {'operation_slug': 'time-reading-clocks'}, name='time_reading_clocks'),
    path('time-days-months-years/', operation_placeholder_view, {'operation_slug': 'time-days-months-years'}, name='time_days_months_years'),
    path('time-timetables/', operation_placeholder_view, {'operation_slug': 'time-timetables'}, name='time_timetables'),
    path('time-calculations/', operation_placeholder_view, {'operation_slug': 'time-calculations'}, name='time_calculations'),
    path('time-converting/', operation_placeholder_view, {'operation_slug': 'time-converting'}, name='time_converting'),

    # Татаал өлчөмдөр > Ылдамдык, аралык жана убакыт (Speed, Distance &
    # Time, promoted to a category) - all 3 new children, none with a
    # real page yet.
    path('speed-distance-time-converting-speeds/', operation_placeholder_view, {'operation_slug': 'speed-distance-time-converting-speeds'}, name='speed_distance_time_converting_speeds'),
    path('speed-distance-time-two-stage-journeys/', operation_placeholder_view, {'operation_slug': 'speed-distance-time-two-stage-journeys'}, name='speed_distance_time_two_stage_journeys'),
    path('speed-distance-time-relative-speeds/', operation_placeholder_view, {'operation_slug': 'speed-distance-time-relative-speeds'}, name='speed_distance_time_relative_speeds'),

    # Стандарттык форма > Көбөйтүү жана бөлүү - both slots, none with a
    # real page yet.
    path('standard-form-multiplying-dividing-calculator/', operation_placeholder_view, {'operation_slug': 'standard-form-multiplying-dividing-calculator'}, name='standard_form_multiplying_dividing_calculator'),
    path('standard-form-multiplying-dividing-non-calculator/', operation_placeholder_view, {'operation_slug': 'standard-form-multiplying-dividing-non-calculator'}, name='standard_form_multiplying_dividing_non_calculator'),

    # Стандарттык форма > Айландыруу - all 3 slots, none with a real
    # page yet.
    path('standard-form-converting-ordinary-to-standard/', operation_placeholder_view, {'operation_slug': 'standard-form-converting-ordinary-to-standard'}, name='standard_form_converting_ordinary_to_standard'),
    path('standard-form-converting-standard-to-ordinary/', operation_placeholder_view, {'operation_slug': 'standard-form-converting-standard-to-ordinary'}, name='standard_form_converting_standard_to_ordinary'),
    path('standard-form-converting-mixed/', operation_placeholder_view, {'operation_slug': 'standard-form-converting-mixed'}, name='standard_form_converting_mixed'),

    # Пропорция > Түз жана тескери пропорция - all 5 slots, none with a
    # real page yet.
    path('direct-inverse-introduction/', operation_placeholder_view, {'operation_slug': 'direct-inverse-introduction'}, name='direct_inverse_introduction'),
    path('direct-inverse-direct/', operation_placeholder_view, {'operation_slug': 'direct-inverse-direct'}, name='direct_inverse_direct'),
    path('direct-inverse-inverse/', operation_placeholder_view, {'operation_slug': 'direct-inverse-inverse'}, name='direct_inverse_inverse'),
    path('direct-inverse-mixed/', operation_placeholder_view, {'operation_slug': 'direct-inverse-mixed'}, name='direct_inverse_mixed'),
    path('direct-inverse-identifying-graphs/', operation_placeholder_view, {'operation_slug': 'direct-inverse-identifying-graphs'}, name='direct_inverse_identifying_graphs'),

    # Пропорция > Графиктер (Graphs) - all 10 slots, none with a real
    # page yet.
    path('graphs-identifying-proportional/', operation_placeholder_view, {'operation_slug': 'graphs-identifying-proportional'}, name='graphs_identifying_proportional'),
    path('graphs-conversion-graphs/', operation_placeholder_view, {'operation_slug': 'graphs-conversion-graphs'}, name='graphs_conversion_graphs'),
    path('graphs-cost-relationships/', operation_placeholder_view, {'operation_slug': 'graphs-cost-relationships'}, name='graphs_cost_relationships'),
    path('graphs-depth-time/', operation_placeholder_view, {'operation_slug': 'graphs-depth-time'}, name='graphs_depth_time'),
    path('graphs-volume-time/', operation_placeholder_view, {'operation_slug': 'graphs-volume-time'}, name='graphs_volume_time'),
    path('graphs-mixed/', operation_placeholder_view, {'operation_slug': 'graphs-mixed'}, name='graphs_mixed'),
    path('graphs-distance-time-constant-speeds/', operation_placeholder_view, {'operation_slug': 'graphs-distance-time-constant-speeds'}, name='graphs_distance_time_constant_speeds'),
    path('graphs-distance-time-variable-speeds/', operation_placeholder_view, {'operation_slug': 'graphs-distance-time-variable-speeds'}, name='graphs_distance_time_variable_speeds'),
    path('graphs-velocity-time/', operation_placeholder_view, {'operation_slug': 'graphs-velocity-time'}, name='graphs_velocity_time'),
    path('graphs-mixed-distance-velocity/', operation_placeholder_view, {'operation_slug': 'graphs-mixed-distance-velocity'}, name='graphs_mixed_distance_velocity'),

    # Графиктер > Айландыруу графиктери - both slots, none with a real
    # page yet.
    path('graphs-conversion-reading/', operation_placeholder_view, {'operation_slug': 'graphs-conversion-reading'}, name='graphs_conversion_reading'),
    path('graphs-conversion-plotting-reading/', operation_placeholder_view, {'operation_slug': 'graphs-conversion-plotting-reading'}, name='graphs_conversion_plotting_reading'),

    # Графиктер > Баа мамилелери - both slots, none with a real page yet.
    path('graphs-cost-introduction/', operation_placeholder_view, {'operation_slug': 'graphs-cost-introduction'}, name='graphs_cost_introduction'),
    path('graphs-cost-with-equations/', operation_placeholder_view, {'operation_slug': 'graphs-cost-with-equations'}, name='graphs_cost_with_equations'),

    # Графиктер > Аралык-убакыт: туруктуу ылдамдыктар - both slots, none
    # with a real page yet.
    path('graphs-distance-time-reading/', operation_placeholder_view, {'operation_slug': 'graphs-distance-time-reading'}, name='graphs_distance_time_reading'),
    path('graphs-distance-time-plotting-reading/', operation_placeholder_view, {'operation_slug': 'graphs-distance-time-plotting-reading'}, name='graphs_distance_time_plotting_reading'),

    # Графиктер > Ылдамдык-убакыт - all 3 slots, none with a real page
    # yet.
    path('graphs-velocity-time-distance/', operation_placeholder_view, {'operation_slug': 'graphs-velocity-time-distance'}, name='graphs_velocity_time_distance'),
    path('graphs-velocity-time-acceleration/', operation_placeholder_view, {'operation_slug': 'graphs-velocity-time-acceleration'}, name='graphs_velocity_time_acceleration'),
    path('graphs-velocity-time-mixed/', operation_placeholder_view, {'operation_slug': 'graphs-velocity-time-mixed'}, name='graphs_velocity_time_mixed'),

    # Пайыздар: калькулятор менен > Туюнтуу - all 3 slots, none with a
    # real page yet.
    path('percentages-expressing-converting-fractions/', operation_placeholder_view, {'operation_slug': 'percentages-expressing-converting-fractions'}, name='percentages_expressing_converting_fractions'),
    path('percentages-expressing-quantity/', operation_placeholder_view, {'operation_slug': 'percentages-expressing-quantity'}, name='percentages_expressing_quantity'),
    path('percentages-expressing-change/', operation_placeholder_view, {'operation_slug': 'percentages-expressing-change'}, name='percentages_expressing_change'),

    # Пайыздар: калькулятор менен > Чоңдуктун пайызы - all 4 slots, none
    # with a real page yet.
    path('percentages-quantity-integer/', operation_placeholder_view, {'operation_slug': 'percentages-quantity-integer'}, name='percentages_quantity_integer'),
    path('percentages-quantity-decimal/', operation_placeholder_view, {'operation_slug': 'percentages-quantity-decimal'}, name='percentages_quantity_decimal'),
    path('percentages-quantity-reverse/', operation_placeholder_view, {'operation_slug': 'percentages-quantity-reverse'}, name='percentages_quantity_reverse'),
    path('percentages-quantity-fpr/', operation_placeholder_view, {'operation_slug': 'percentages-quantity-fpr'}, name='percentages_quantity_fpr'),

    # Пайыздар: калькулятор менен > Көбөйтүү жана азайтуу - all 7 slots,
    # none with a real page yet.
    path('percentages-incdec-increase/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-increase'}, name='percentages_incdec_increase'),
    path('percentages-incdec-decrease/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-decrease'}, name='percentages_incdec_decrease'),
    path('percentages-incdec-mixed/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-mixed'}, name='percentages_incdec_mixed'),
    path('percentages-incdec-simple-interest/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-simple-interest'}, name='percentages_incdec_simple_interest'),
    path('percentages-incdec-using-multiplier/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-using-multiplier'}, name='percentages_incdec_using_multiplier'),
    path('percentages-incdec-reverse/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-reverse'}, name='percentages_incdec_reverse'),
    path('percentages-incdec-marginal-tax/', operation_placeholder_view, {'operation_slug': 'percentages-incdec-marginal-tax'}, name='percentages_incdec_marginal_tax'),

    # Пайыздар: калькулятор менен > Кайталанма пайыздык өзгөрүү - all 5
    # slots, none with a real page yet.
    path('percentages-repeated-change-increase-compound-interest/', operation_placeholder_view, {'operation_slug': 'percentages-repeated-change-increase-compound-interest'}, name='percentages_repeated_change_increase_compound_interest'),
    path('percentages-repeated-change-decrease/', operation_placeholder_view, {'operation_slug': 'percentages-repeated-change-decrease'}, name='percentages_repeated_change_decrease'),
    path('percentages-repeated-change-increase-decrease/', operation_placeholder_view, {'operation_slug': 'percentages-repeated-change-increase-decrease'}, name='percentages_repeated_change_increase_decrease'),
    path('percentages-repeated-change-reverse/', operation_placeholder_view, {'operation_slug': 'percentages-repeated-change-reverse'}, name='percentages_repeated_change_reverse'),
    path('percentages-repeated-change-mixed/', operation_placeholder_view, {'operation_slug': 'percentages-repeated-change-mixed'}, name='percentages_repeated_change_mixed'),

    # Пайыздар: калькуляторсуз > Туюнтуу - 2 flat slots (Converting
    # Fractions is mirrored in, not a URL here).
    path('percentages-noncalc-expressing-quantity/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-expressing-quantity'}, name='percentages_noncalc_expressing_quantity'),
    path('percentages-noncalc-expressing-change/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-expressing-change'}, name='percentages_noncalc_expressing_change'),

    # Пайыздар: калькуляторсуз > Чоңдуктун пайызы - all 6 slots, none
    # with a real page yet.
    path('percentages-noncalc-quantity-10s/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-quantity-10s'}, name='percentages_noncalc_quantity_10s'),
    path('percentages-noncalc-quantity-5s/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-quantity-5s'}, name='percentages_noncalc_quantity_5s'),
    path('percentages-noncalc-quantity-integer-decimal/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-quantity-integer-decimal'}, name='percentages_noncalc_quantity_integer_decimal'),
    path('percentages-noncalc-quantity-reverse/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-quantity-reverse'}, name='percentages_noncalc_quantity_reverse'),
    path('percentages-noncalc-quantity-fpr/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-quantity-fpr'}, name='percentages_noncalc_quantity_fpr'),
    path('percentages-noncalc-quantity-fpr-frequency-trees/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-quantity-fpr-frequency-trees'}, name='percentages_noncalc_quantity_fpr_frequency_trees'),

    # Пайыздар: калькуляторсуз > Көбөйтүү жана азайтуу - all 4 slots,
    # none with a real page yet.
    path('percentages-noncalc-incdec-increase/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-incdec-increase'}, name='percentages_noncalc_incdec_increase'),
    path('percentages-noncalc-incdec-decrease/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-incdec-decrease'}, name='percentages_noncalc_incdec_decrease'),
    path('percentages-noncalc-incdec-mixed/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-incdec-mixed'}, name='percentages_noncalc_incdec_mixed'),
    path('percentages-noncalc-incdec-reverse/', operation_placeholder_view, {'operation_slug': 'percentages-noncalc-incdec-reverse'}, name='percentages_noncalc_incdec_reverse'),

    # Катыш > Туюнтуу - all 3 slots, none with a real page yet.
    path('ratio-expressing-division/', operation_placeholder_view, {'operation_slug': 'ratio-expressing-division'}, name='ratio_expressing_division'),
    path('ratio-expressing-simplifying/', operation_placeholder_view, {'operation_slug': 'ratio-expressing-simplifying'}, name='ratio_expressing_simplifying'),
    path('ratio-expressing-1-to-n/', operation_placeholder_view, {'operation_slug': 'ratio-expressing-1-to-n'}, name='ratio_expressing_1_to_n'),

    # Катыш > Катыштар жана чоңдуктар - all 7 flat leaves.
    path('ratio-dividing-into-a-ratio/', operation_placeholder_view, {'operation_slug': 'ratio-dividing-into-a-ratio'}, name='ratio_dividing_into_a_ratio'),
    path('ratio-quantities-reverse/', operation_placeholder_view, {'operation_slug': 'ratio-quantities-reverse'}, name='ratio_quantities_reverse'),
    path('ratio-quantities-mixed/', operation_placeholder_view, {'operation_slug': 'ratio-quantities-mixed'}, name='ratio_quantities_mixed'),
    path('ratio-dividing-with-line-segments/', operation_placeholder_view, {'operation_slug': 'ratio-dividing-with-line-segments'}, name='ratio_dividing_with_line_segments'),
    path('ratio-dividing-fpr-calculator/', operation_placeholder_view, {'operation_slug': 'ratio-dividing-fpr-calculator'}, name='ratio_dividing_fpr_calculator'),
    path('ratio-dividing-fpr-non-calculator/', operation_placeholder_view, {'operation_slug': 'ratio-dividing-fpr-non-calculator'}, name='ratio_dividing_fpr_non_calculator'),
    path('ratio-dividing-fpr-frequency-trees/', operation_placeholder_view, {'operation_slug': 'ratio-dividing-fpr-frequency-trees'}, name='ratio_dividing_fpr_frequency_trees'),

    # Катыш > Түрлөндүрүү - all 4 slots, none with a real page yet.
    path('ratio-manipulation-1-to-n/', operation_placeholder_view, {'operation_slug': 'ratio-manipulation-1-to-n'}, name='ratio_manipulation_1_to_n'),
    path('ratio-manipulation-comparing-parts/', operation_placeholder_view, {'operation_slug': 'ratio-manipulation-comparing-parts'}, name='ratio_manipulation_comparing_parts'),
    path('ratio-manipulation-combining/', operation_placeholder_view, {'operation_slug': 'ratio-manipulation-combining'}, name='ratio_manipulation_combining'),
    path('ratio-manipulation-changing/', operation_placeholder_view, {'operation_slug': 'ratio-manipulation-changing'}, name='ratio_manipulation_changing'),

    # Катыш > Аралаш - both slots, none with a real page yet.
    path('ratio-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'ratio-mixed-foundation'}, name='ratio_mixed_foundation'),
    path('ratio-mixed-higher/', operation_placeholder_view, {'operation_slug': 'ratio-mixed-higher'}, name='ratio_mixed_higher'),

    # Турмуштук колдонуулар > Баалар - both slots, none with a real
    # page yet.
    path('real-life-prices-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-prices-calculator'}, name='real_life_prices_calculator'),
    path('real-life-prices-non-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-prices-non-calculator'}, name='real_life_prices_non_calculator'),

    # Турмуштук колдонуулар > Пайдалуу сатып алуу - both slots, none
    # with a real page yet.
    path('real-life-best-buys-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-best-buys-calculator'}, name='real_life_best_buys_calculator'),
    path('real-life-best-buys-non-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-best-buys-non-calculator'}, name='real_life_best_buys_non_calculator'),

    # Турмуштук колдонуулар > Валюта курстары - both slots, none with a
    # real page yet.
    path('real-life-exchange-rates-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-exchange-rates-calculator'}, name='real_life_exchange_rates_calculator'),
    path('real-life-exchange-rates-non-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-exchange-rates-non-calculator'}, name='real_life_exchange_rates_non_calculator'),

    # Турмуштук колдонуулар > Рецепттер - both slots, none with a real
    # page yet.
    path('real-life-recipes-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-recipes-calculator'}, name='real_life_recipes_calculator'),
    path('real-life-recipes-non-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-recipes-non-calculator'}, name='real_life_recipes_non_calculator'),

    # Турмуштук колдонуулар > Аралаш - both slots, none with a real
    # page yet.
    path('real-life-mixed-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-mixed-calculator'}, name='real_life_mixed_calculator'),
    path('real-life-mixed-non-calculator/', operation_placeholder_view, {'operation_slug': 'real-life-mixed-non-calculator'}, name='real_life_mixed_non_calculator'),

    # Алгебра > Киришүү - all 3 flat slots, none with a real page yet.
    path('algebra-intro-definitions/', operation_placeholder_view, {'operation_slug': 'algebra-intro-definitions'}, name='algebra_intro_definitions'),
    path('algebra-intro-notation/', operation_placeholder_view, {'operation_slug': 'algebra-intro-notation'}, name='algebra_intro_notation'),
    path('algebra-intro-manipulating-formulae/', operation_placeholder_view, {'operation_slug': 'algebra-intro-manipulating-formulae'}, name='algebra_intro_manipulating_formulae'),

    # Алгебра > Киришүү > Туюнтмаларды түзүү - all 3 slots, none with a
    # real page yet.
    path('algebra-forming-expr-function-machines/', operation_placeholder_view, {'operation_slug': 'algebra-forming-expr-function-machines'}, name='algebra_forming_expr_function_machines'),
    path('algebra-forming-expr-linear/', operation_placeholder_view, {'operation_slug': 'algebra-forming-expr-linear'}, name='algebra_forming_expr_linear'),
    path('algebra-forming-expr-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-forming-expr-quadratic'}, name='algebra_forming_expr_quadratic'),

    # Алгебра > Теңдемелер: сызыктуу - all 8 flat slots, none with a
    # real page yet.
    path('algebra-linear-forming/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming'}, name='algebra_linear_forming'),
    path('algebra-linear-variable-one-side-calculator/', operation_placeholder_view, {'operation_slug': 'algebra-linear-variable-one-side-calculator'}, name='algebra_linear_variable_one_side_calculator'),
    path('algebra-linear-variable-one-side-non-calculator/', operation_placeholder_view, {'operation_slug': 'algebra-linear-variable-one-side-non-calculator'}, name='algebra_linear_variable_one_side_non_calculator'),
    path('algebra-linear-variable-both-sides/', operation_placeholder_view, {'operation_slug': 'algebra-linear-variable-both-sides'}, name='algebra_linear_variable_both_sides'),
    path('algebra-linear-rational/', operation_placeholder_view, {'operation_slug': 'algebra-linear-rational'}, name='algebra_linear_rational'),
    path('algebra-linear-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-linear-mixed'}, name='algebra_linear_mixed'),
    path('algebra-linear-inequalities/', operation_placeholder_view, {'operation_slug': 'algebra-linear-inequalities'}, name='algebra_linear_inequalities'),
    path('algebra-linear-unknown-indices/', operation_placeholder_view, {'operation_slug': 'algebra-linear-unknown-indices'}, name='algebra_linear_unknown_indices'),

    # Алгебра > Теңдемелер: квадраттык - all 13 slots, none with a real
    # page yet.
    path('algebra-quadratic-forming/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-forming'}, name='algebra_quadratic_forming'),
    path('algebra-quadratic-factorisation-double-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-factorisation-double-brackets'}, name='algebra_quadratic_factorisation_double_brackets'),
    path('algebra-quadratic-b-zero/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero'}, name='algebra_quadratic_b_zero'),
    path('algebra-quadratic-c-zero/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-c-zero'}, name='algebra_quadratic_c_zero'),
    path('algebra-quadratic-completing-square/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-completing-square'}, name='algebra_quadratic_completing_square'),
    path('algebra-quadratic-rational/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-rational'}, name='algebra_quadratic_rational'),
    path('algebra-quadratic-formula/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-formula'}, name='algebra_quadratic_formula'),
    path('algebra-quadratic-no-solution/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-no-solution'}, name='algebra_quadratic_no_solution'),
    path('algebra-quadratic-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-mixed'}, name='algebra_quadratic_mixed'),
    path('algebra-quadratic-trial-improvement/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-trial-improvement'}, name='algebra_quadratic_trial_improvement'),
    path('algebra-quadratic-iteration/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-iteration'}, name='algebra_quadratic_iteration'),
    path('algebra-quadratic-by-intersection/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-by-intersection'}, name='algebra_quadratic_by_intersection'),
    path('algebra-quadratic-inequalities/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-inequalities'}, name='algebra_quadratic_inequalities'),

    # Алгебра > Теңдемелер: системасы - all 5 flat slots, none with a
    # real page yet.
    path('algebra-simultaneous-forming/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-forming'}, name='algebra_simultaneous_forming'),
    path('algebra-simultaneous-substitution/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-substitution'}, name='algebra_simultaneous_substitution'),
    path('algebra-simultaneous-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-mixed'}, name='algebra_simultaneous_mixed'),
    path('algebra-simultaneous-graphically/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-graphically'}, name='algebra_simultaneous_graphically'),
    path('algebra-simultaneous-linear-non-linear/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-linear-non-linear'}, name='algebra_simultaneous_linear_non_linear'),

    # Теңдемелер: сызыктуу > Кашаа менен - all 3 slots, none with a
    # real page yet.
    path('algebra-linear-brackets-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-linear-brackets-without-coefficients'}, name='algebra_linear_brackets_without_coefficients'),
    path('algebra-linear-brackets-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-linear-brackets-with-coefficients'}, name='algebra_linear_brackets_with_coefficients'),
    path('algebra-linear-brackets-multiple/', operation_placeholder_view, {'operation_slug': 'algebra-linear-brackets-multiple'}, name='algebra_linear_brackets_multiple'),

    # Теңдемелер: сызыктуу > Түзүү - all 3 slots, none with a real page
    # yet.
    path('algebra-linear-forming-shapes-angles-real-life/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming-shapes-angles-real-life'}, name='algebra_linear_forming_shapes_angles_real_life'),
    path('algebra-linear-forming-function-machines/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming-function-machines'}, name='algebra_linear_forming_function_machines'),
    path('algebra-linear-forming-functions-sequences/', operation_placeholder_view, {'operation_slug': 'algebra-linear-forming-functions-sequences'}, name='algebra_linear_forming_functions_sequences'),

    # Теңдемелер: сызыктуу > Белгисиз бир жагында: калькулятор менен -
    # all 4 slots, none with a real page yet.
    path('algebra-linear-var1side-calc-1step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-1step'}, name='algebra_linear_var1side_calc_1step'),
    path('algebra-linear-var1side-calc-2step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-2step'}, name='algebra_linear_var1side_calc_2step'),
    path('algebra-linear-var1side-calc-3step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-3step'}, name='algebra_linear_var1side_calc_3step'),
    path('algebra-linear-var1side-calc-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-calc-mixed'}, name='algebra_linear_var1side_calc_mixed'),

    # Теңдемелер: сызыктуу > Белгисиз бир жагында: калькуляторсуз - all
    # 4 slots, none with a real page yet.
    path('algebra-linear-var1side-noncalc-1step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-1step'}, name='algebra_linear_var1side_noncalc_1step'),
    path('algebra-linear-var1side-noncalc-2step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-2step'}, name='algebra_linear_var1side_noncalc_2step'),
    path('algebra-linear-var1side-noncalc-3step/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-3step'}, name='algebra_linear_var1side_noncalc_3step'),
    path('algebra-linear-var1side-noncalc-rational/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var1side-noncalc-rational'}, name='algebra_linear_var1side_noncalc_rational'),

    # Теңдемелер: сызыктуу > Белгисиз эки жагында - all 4 slots, none
    # with a real page yet.
    path('algebra-linear-var-both-sides-without-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-without-brackets'}, name='algebra_linear_var_both_sides_without_brackets'),
    path('algebra-linear-var-both-sides-with-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-with-brackets'}, name='algebra_linear_var_both_sides_with_brackets'),
    path('algebra-linear-var-both-sides-graphical-intersections/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-graphical-intersections'}, name='algebra_linear_var_both_sides_graphical_intersections'),
    path('algebra-linear-var-both-sides-parallel-lines/', operation_placeholder_view, {'operation_slug': 'algebra-linear-var-both-sides-parallel-lines'}, name='algebra_linear_var_both_sides_parallel_lines'),

    # Теңдемелер: квадраттык > Көбөйтүүчүлөргө ажыратуу: эки кашаа
    # менен - both slots, none with a real page yet.
    path('algebra-quadratic-factorisation-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-factorisation-without-coefficients'}, name='algebra_quadratic_factorisation_without_coefficients'),
    path('algebra-quadratic-factorisation-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-factorisation-with-coefficients'}, name='algebra_quadratic_factorisation_with_coefficients'),

    # Теңдемелер: квадраттык > b = 0 - all 3 slots, none with a real
    # page yet.
    path('algebra-quadratic-b-zero-rearranging/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero-rearranging'}, name='algebra_quadratic_b_zero_rearranging'),
    path('algebra-quadratic-b-zero-difference-of-squares/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero-difference-of-squares'}, name='algebra_quadratic_b_zero_difference_of_squares'),
    path('algebra-quadratic-b-zero-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-b-zero-mixed'}, name='algebra_quadratic_b_zero_mixed'),

    # Теңдемелер: квадраттык > Рационалдык - both slots, none with a
    # real page yet.
    path('algebra-quadratic-rational-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-rational-without-coefficients'}, name='algebra_quadratic_rational_without_coefficients'),
    path('algebra-quadratic-rational-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-quadratic-rational-with-coefficients'}, name='algebra_quadratic_rational_with_coefficients'),

    # Теңдемелер: системасы > Жоюу ыкмасы - all 3 slots, none with a
    # real page yet.
    path('algebra-simultaneous-elimination-without-balancing/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-elimination-without-balancing'}, name='algebra_simultaneous_elimination_without_balancing'),
    path('algebra-simultaneous-elimination-with-balancing/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-elimination-with-balancing'}, name='algebra_simultaneous_elimination_with_balancing'),
    path('algebra-simultaneous-elimination-negative-only/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-elimination-negative-only'}, name='algebra_simultaneous_elimination_negative_only'),

    # Теңдемелер: системасы > Сызыктуу жана сызыктуу эмес - both slots,
    # none with a real page yet.
    path('algebra-simultaneous-linear-non-linear-algebraically/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-linear-non-linear-algebraically'}, name='algebra_simultaneous_linear_non_linear_algebraically'),
    path('algebra-simultaneous-linear-non-linear-graphically/', operation_placeholder_view, {'operation_slug': 'algebra-simultaneous-linear-non-linear-graphically'}, name='algebra_simultaneous_linear_non_linear_graphically'),

    # Функциялар - "IGCSE" flat slot, none with a real page yet.
    path('algebra-functions-igcse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-igcse'}, name='algebra_functions_igcse'),

    # Функциялар > Түзүү - all 7 slots, none with a real page yet.
    path('algebra-functions-forming-expressions/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-expressions'}, name='algebra_functions_forming_expressions'),
    path('algebra-functions-forming-simple-functions/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-simple-functions'}, name='algebra_functions_forming_simple_functions'),
    path('algebra-functions-forming-changing-subject/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-changing-subject'}, name='algebra_functions_forming_changing_subject'),
    path('algebra-functions-forming-composite-linear/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-composite-linear'}, name='algebra_functions_forming_composite_linear'),
    path('algebra-functions-forming-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-inverse'}, name='algebra_functions_forming_inverse'),
    path('algebra-functions-forming-composite-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-composite-inverse'}, name='algebra_functions_forming_composite_inverse'),
    path('algebra-functions-forming-composite-quadratics/', operation_placeholder_view, {'operation_slug': 'algebra-functions-forming-composite-quadratics'}, name='algebra_functions_forming_composite_quadratics'),

    # Функциялар > Маанисин эсептөө - all 10 slots, none with a real
    # page yet.
    path('algebra-functions-evaluating-simple-machines/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-simple-machines'}, name='algebra_functions_evaluating_simple_machines'),
    path('algebra-functions-evaluating-graphing/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-graphing'}, name='algebra_functions_evaluating_graphing'),
    path('algebra-functions-evaluating-equations-sequences/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-equations-sequences'}, name='algebra_functions_evaluating_equations_sequences'),
    path('algebra-functions-evaluating-linear/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-linear'}, name='algebra_functions_evaluating_linear'),
    path('algebra-functions-evaluating-indices/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-indices'}, name='algebra_functions_evaluating_indices'),
    path('algebra-functions-evaluating-composite/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-composite'}, name='algebra_functions_evaluating_composite'),
    path('algebra-functions-evaluating-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-inverse'}, name='algebra_functions_evaluating_inverse'),
    path('algebra-functions-evaluating-composite-inverse/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-composite-inverse'}, name='algebra_functions_evaluating_composite_inverse'),
    path('algebra-functions-evaluating-solving-equations/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-solving-equations'}, name='algebra_functions_evaluating_solving_equations'),
    path('algebra-functions-evaluating-iteration/', operation_placeholder_view, {'operation_slug': 'algebra-functions-evaluating-iteration'}, name='algebra_functions_evaluating_iteration'),

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

    # Question bank / online tests
    path('questions/', question_bank_view, name='question_bank'),
    path('questions/create/', question_create_view, name='question_create'),
    path('tests/', exam_list_view, name='exam_list'),
    path('tests/create/', exam_create_view, name='exam_create'),
    path('tests/<int:pk>/', exam_detail_view, name='exam_detail'),
    path('t/<str:access_code>/', exam_take_view, name='exam_take'),
    path('t/<str:access_code>/submit/', exam_submit_view, name='exam_submit'),
    path('t/<str:access_code>/result/<int:attempt_id>/', exam_result_view, name='exam_result'),

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
else:
    # Static files are served by WhiteNoise in production, but uploaded
    # media isn't unless S3/R2-compatible storage is configured (see
    # PERSISTENT_MEDIA_STORAGE_CONFIGURED). Serve it from the local
    # (Railway volume-backed) MEDIA_ROOT as a fallback so uploads like
    # payment QR codes and resource thumbnails actually load.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]