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

    # Графиктер: абстракттуу - 5 flat slots, none with a real page yet.
    path('algebra-graphs-abstract-coordinates/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates'}, name='algebra_graphs_abstract_coordinates'),
    path('algebra-graphs-abstract-linear-calculating/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calculating'}, name='algebra_graphs_abstract_linear_calculating'),
    path('algebra-graphs-abstract-linear-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plotting'}, name='algebra_graphs_abstract_linear_plotting'),
    path('algebra-graphs-abstract-linear-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-reading'}, name='algebra_graphs_abstract_linear_reading'),
    path('algebra-graphs-abstract-linear-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-mixed'}, name='algebra_graphs_abstract_linear_mixed'),

    # Графиктер: турмуштук - 4 flat slots, none with a real page yet.
    path('algebra-graphs-real-life-depth-time/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-depth-time'}, name='algebra_graphs_real_life_depth_time'),
    path('algebra-graphs-real-life-volume-time/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-volume-time'}, name='algebra_graphs_real_life_volume_time'),
    path('algebra-graphs-real-life-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-mixed'}, name='algebra_graphs_real_life_mixed'),
    path('algebra-graphs-real-life-mixed-distance-velocity/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-mixed-distance-velocity'}, name='algebra_graphs_real_life_mixed_distance_velocity'),

    # Барабарсыздыктар - 2 flat slots, none with a real page yet.
    path('algebra-inequalities-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-quadratic'}, name='algebra_inequalities_quadratic'),
    path('algebra-inequalities-trial-improvement/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-trial-improvement'}, name='algebra_inequalities_trial_improvement'),

    # Түрлөндүрүү - 2 flat slots, none with a real page yet.
    path('algebra-manipulation-notation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation'}, name='algebra_manipulation_notation'),
    path('algebra-manipulation-changing-subject/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject'}, name='algebra_manipulation_changing_subject'),

    # Ырааттуулуктар - 9 flat slots, none with a real page yet.
    path('algebra-sequences-introduction/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-introduction'}, name='algebra_sequences_introduction'),
    path('algebra-sequences-with-graphs/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-with-graphs'}, name='algebra_sequences_with_graphs'),
    path('algebra-sequences-equations-functions/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-equations-functions'}, name='algebra_sequences_equations_functions'),
    path('algebra-sequences-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-quadratic'}, name='algebra_sequences_quadratic'),
    path('algebra-sequences-linear-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-quadratic'}, name='algebra_sequences_linear_quadratic'),
    path('algebra-sequences-geometric/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-geometric'}, name='algebra_sequences_geometric'),
    path('algebra-sequences-fibonacci/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-fibonacci'}, name='algebra_sequences_fibonacci'),
    path('algebra-sequences-special/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-special'}, name='algebra_sequences_special'),
    path('algebra-sequences-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-mixed'}, name='algebra_sequences_mixed'),

    # Ордуна коюу (renamed from "Коюу") - 2 flat slots, none with a
    # real page yet.
    path('algebra-substitution-with-calculator/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-with-calculator'}, name='algebra_substitution_with_calculator'),
    path('algebra-substitution-vectors/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-vectors'}, name='algebra_substitution_vectors'),

    # Ордуна коюу > Белгилерди колдонуу / Даражасыз / Даража менен - 6
    # distinct Positive/Negative slots plus 1 shared Mixed slot.
    path('algebra-substitution-symbols-positive/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-symbols-positive'}, name='algebra_substitution_symbols_positive'),
    path('algebra-substitution-symbols-negative/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-symbols-negative'}, name='algebra_substitution_symbols_negative'),
    path('algebra-substitution-without-indices-positive/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-without-indices-positive'}, name='algebra_substitution_without_indices_positive'),
    path('algebra-substitution-without-indices-negative/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-without-indices-negative'}, name='algebra_substitution_without_indices_negative'),
    path('algebra-substitution-with-indices-positive/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-with-indices-positive'}, name='algebra_substitution_with_indices_positive'),
    path('algebra-substitution-with-indices-negative/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-with-indices-negative'}, name='algebra_substitution_with_indices_negative'),
    path('algebra-substitution-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-substitution-mixed'}, name='algebra_substitution_mixed'),

    # Графиктер: абстракттуу > Координаттар - all 6 slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-coordinates-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-reading'}, name='algebra_graphs_abstract_coordinates_reading'),
    path('algebra-graphs-abstract-coordinates-reading-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-reading-plotting'}, name='algebra_graphs_abstract_coordinates_reading_plotting'),
    path('algebra-graphs-abstract-coordinates-midpoint-endpoint/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-midpoint-endpoint'}, name='algebra_graphs_abstract_coordinates_midpoint_endpoint'),
    path('algebra-graphs-abstract-coordinates-segments-ratio/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-segments-ratio'}, name='algebra_graphs_abstract_coordinates_segments_ratio'),
    path('algebra-graphs-abstract-coordinates-geometric-problems/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-geometric-problems'}, name='algebra_graphs_abstract_coordinates_geometric_problems'),
    path('algebra-graphs-abstract-coordinates-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-coordinates-with-pythagoras'}, name='algebra_graphs_abstract_coordinates_with_pythagoras'),

    # Графиктер: абстракттуу > Сызыктуу: эсептөө - 9 flat slots, none
    # with a real page yet.
    path('algebra-graphs-abstract-linear-calc-functions-graphs/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-functions-graphs'}, name='algebra_graphs_abstract_linear_calc_functions_graphs'),
    path('algebra-graphs-abstract-linear-calc-gradient-intercept/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-gradient-intercept'}, name='algebra_graphs_abstract_linear_calc_gradient_intercept'),
    path('algebra-graphs-abstract-linear-calc-evaluating-coordinates/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-evaluating-coordinates'}, name='algebra_graphs_abstract_linear_calc_evaluating_coordinates'),
    path('algebra-graphs-abstract-linear-calc-evaluating-intersections/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-evaluating-intersections'}, name='algebra_graphs_abstract_linear_calc_evaluating_intersections'),
    path('algebra-graphs-abstract-linear-calc-parallel/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-parallel'}, name='algebra_graphs_abstract_linear_calc_parallel'),
    path('algebra-graphs-abstract-linear-calc-perpendicular/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-perpendicular'}, name='algebra_graphs_abstract_linear_calc_perpendicular'),
    path('algebra-graphs-abstract-linear-calc-parallel-perpendicular/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-parallel-perpendicular'}, name='algebra_graphs_abstract_linear_calc_parallel_perpendicular'),
    path('algebra-graphs-abstract-linear-calc-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-mixed'}, name='algebra_graphs_abstract_linear_calc_mixed'),
    path('algebra-graphs-abstract-linear-calc-identifying-graphs/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-calc-identifying-graphs'}, name='algebra_graphs_abstract_linear_calc_identifying_graphs'),

    # Графиктер: абстракттуу > Сызыктуу: чиймелөө - all 8 slots, none
    # with a real page yet.
    path('algebra-graphs-abstract-linear-plot-with-functions/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-with-functions'}, name='algebra_graphs_abstract_linear_plot_with_functions'),
    path('algebra-graphs-abstract-linear-plot-with-sequences/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-with-sequences'}, name='algebra_graphs_abstract_linear_plot_with_sequences'),
    path('algebra-graphs-abstract-linear-plot-cover-up/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-cover-up'}, name='algebra_graphs_abstract_linear_plot_cover_up'),
    path('algebra-graphs-abstract-linear-plot-gradient/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-gradient'}, name='algebra_graphs_abstract_linear_plot_gradient'),
    path('algebra-graphs-abstract-linear-plot-gradient-intercept-method/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-gradient-intercept-method'}, name='algebra_graphs_abstract_linear_plot_gradient_intercept_method'),
    path('algebra-graphs-abstract-linear-plot-table-of-values/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-table-of-values'}, name='algebra_graphs_abstract_linear_plot_table_of_values'),
    path('algebra-graphs-abstract-linear-plot-inequalities/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-inequalities'}, name='algebra_graphs_abstract_linear_plot_inequalities'),
    path('algebra-graphs-abstract-linear-plot-simultaneous/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-plot-simultaneous'}, name='algebra_graphs_abstract_linear_plot_simultaneous'),

    # Графиктер: абстракттуу > Сызыктуу: окуу - only 4 slots built so
    # far (reference screenshot was cut off, flagged to the user).
    path('algebra-graphs-abstract-linear-read-horizontal-vertical/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-horizontal-vertical'}, name='algebra_graphs_abstract_linear_read_horizontal_vertical'),
    path('algebra-graphs-abstract-linear-read-gradient/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-gradient'}, name='algebra_graphs_abstract_linear_read_gradient'),
    path('algebra-graphs-abstract-linear-read-equation/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-equation'}, name='algebra_graphs_abstract_linear_read_equation'),
    path('algebra-graphs-abstract-linear-read-evaluating-intersections/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-linear-read-evaluating-intersections'}, name='algebra_graphs_abstract_linear_read_evaluating_intersections'),

    # Графиктер: абстракттуу > Квадраттык - all 5 slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-quadratic-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-plotting'}, name='algebra_graphs_abstract_quadratic_plotting'),
    path('algebra-graphs-abstract-quadratic-significant-points/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-significant-points'}, name='algebra_graphs_abstract_quadratic_significant_points'),
    path('algebra-graphs-abstract-quadratic-turning-points/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-turning-points'}, name='algebra_graphs_abstract_quadratic_turning_points'),
    path('algebra-graphs-abstract-quadratic-solving-by-intersection/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-solving-by-intersection'}, name='algebra_graphs_abstract_quadratic_solving_by_intersection'),
    path('algebra-graphs-abstract-quadratic-simultaneous/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-quadratic-simultaneous'}, name='algebra_graphs_abstract_quadratic_simultaneous'),

    # Графиктер: абстракттуу > Тегеректер - both slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-circles-equation/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-circles-equation'}, name='algebra_graphs_abstract_circles_equation'),
    path('algebra-graphs-abstract-circles-tangent/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-circles-tangent'}, name='algebra_graphs_abstract_circles_tangent'),

    # Графиктер: абстракттуу > Башка сызыктуу эмес - all 6 slots, none
    # with a real page yet.
    path('algebra-graphs-abstract-other-nonlinear-plotting/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-plotting'}, name='algebra_graphs_abstract_other_nonlinear_plotting'),
    path('algebra-graphs-abstract-other-nonlinear-identifying-nonlinear/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-identifying-nonlinear'}, name='algebra_graphs_abstract_other_nonlinear_identifying_nonlinear'),
    path('algebra-graphs-abstract-other-nonlinear-identifying-proportional/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-identifying-proportional'}, name='algebra_graphs_abstract_other_nonlinear_identifying_proportional'),
    path('algebra-graphs-abstract-other-nonlinear-estimating-gradient/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-estimating-gradient'}, name='algebra_graphs_abstract_other_nonlinear_estimating_gradient'),
    path('algebra-graphs-abstract-other-nonlinear-exponential-functions/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-exponential-functions'}, name='algebra_graphs_abstract_other_nonlinear_exponential_functions'),
    path('algebra-graphs-abstract-other-nonlinear-trig-functions/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-other-nonlinear-trig-functions'}, name='algebra_graphs_abstract_other_nonlinear_trig_functions'),

    # Графиктер: абстракттуу > Түрлөндүрүүлөр - both slots, none with a
    # real page yet.
    path('algebra-graphs-abstract-transformations-gcse/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-transformations-gcse'}, name='algebra_graphs_abstract_transformations_gcse'),
    path('algebra-graphs-abstract-transformations-igcse/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-abstract-transformations-igcse'}, name='algebra_graphs_abstract_transformations_igcse'),

    # Графиктер: турмуштук > Айландыруу графиктери - 2 confirmed slots
    # (reference screenshot was cut off after these).
    path('algebra-graphs-real-life-conversion-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-conversion-reading'}, name='algebra_graphs_real_life_conversion_reading'),
    path('algebra-graphs-real-life-conversion-plotting-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-conversion-plotting-reading'}, name='algebra_graphs_real_life_conversion_plotting_reading'),

    # Графиктер: турмуштук > Баа катыштары - 2 confirmed slots (cut off
    # in the reference).
    path('algebra-graphs-real-life-cost-introduction/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-cost-introduction'}, name='algebra_graphs_real_life_cost_introduction'),
    path('algebra-graphs-real-life-cost-with-equations/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-cost-with-equations'}, name='algebra_graphs_real_life_cost_with_equations'),

    # Графиктер: турмуштук > Аралык-Убакыт: турактуу ылдамдык - 2
    # confirmed slots (cut off in the reference).
    path('algebra-graphs-real-life-distance-time-constant-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-distance-time-constant-reading'}, name='algebra_graphs_real_life_distance_time_constant_reading'),
    path('algebra-graphs-real-life-distance-time-constant-plotting-reading/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-distance-time-constant-plotting-reading'}, name='algebra_graphs_real_life_distance_time_constant_plotting_reading'),

    # Графиктер: турмуштук > Ылдамдык-Убакыт - all 3 slots, none with a
    # real page yet.
    path('algebra-graphs-real-life-velocity-time-distance/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-velocity-time-distance'}, name='algebra_graphs_real_life_velocity_time_distance'),
    path('algebra-graphs-real-life-velocity-time-acceleration/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-velocity-time-acceleration'}, name='algebra_graphs_real_life_velocity_time_acceleration'),
    path('algebra-graphs-real-life-velocity-time-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-graphs-real-life-velocity-time-mixed'}, name='algebra_graphs_real_life_velocity_time_mixed'),

    # Барабарсыздыктар > Сызыктуу - all 6 slots, none with a real page
    # yet.
    path('algebra-inequalities-linear-forming/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-forming'}, name='algebra_inequalities_linear_forming'),
    path('algebra-inequalities-linear-evaluating/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-evaluating'}, name='algebra_inequalities_linear_evaluating'),
    path('algebra-inequalities-linear-representing/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-representing'}, name='algebra_inequalities_linear_representing'),
    path('algebra-inequalities-linear-solving-single/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-solving-single'}, name='algebra_inequalities_linear_solving_single'),
    path('algebra-inequalities-linear-solving-single-double/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-solving-single-double'}, name='algebra_inequalities_linear_solving_single_double'),
    path('algebra-inequalities-linear-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-linear-mixed'}, name='algebra_inequalities_linear_mixed'),

    # Барабарсыздыктар > Графикалык - 2 confirmed slots (cut off in the
    # reference).
    path('algebra-inequalities-graphical-shade-wanted/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-graphical-shade-wanted'}, name='algebra_inequalities_graphical_shade_wanted'),
    path('algebra-inequalities-graphical-shade-unwanted/', operation_placeholder_view, {'operation_slug': 'algebra-inequalities-graphical-shade-unwanted'}, name='algebra_inequalities_graphical_shade_unwanted'),

    # Түрлөндүрүү > Туюнтма түзүү - all 3 slots, none with a real page
    # yet.
    path('algebra-manipulation-forming-function-machines/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-forming-function-machines'}, name='algebra_manipulation_forming_function_machines'),
    path('algebra-manipulation-forming-linear/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-forming-linear'}, name='algebra_manipulation_forming_linear'),
    path('algebra-manipulation-forming-quadratic/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-forming-quadratic'}, name='algebra_manipulation_forming_quadratic'),

    # Түрлөндүрүү > Алгебралык бөлчөктөр - all 6 slots, none with a
    # real page yet.
    path('algebra-manipulation-fractions-adding-subtracting/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-adding-subtracting'}, name='algebra_manipulation_fractions_adding_subtracting'),
    path('algebra-manipulation-fractions-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-multiplying-dividing'}, name='algebra_manipulation_fractions_multiplying_dividing'),
    path('algebra-manipulation-fractions-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-mixed'}, name='algebra_manipulation_fractions_mixed'),
    path('algebra-manipulation-fractions-simplifying/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-simplifying'}, name='algebra_manipulation_fractions_simplifying'),
    path('algebra-manipulation-fractions-simplifying-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-simplifying-with-factorisation'}, name='algebra_manipulation_fractions_simplifying_with_factorisation'),
    path('algebra-manipulation-fractions-simplifying-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-fractions-simplifying-difference-squares'}, name='algebra_manipulation_fractions_simplifying_difference_squares'),

    # Түрлөндүрүү > Формуланын өзгөрмөсүн алмаштыруу - all 4 slots,
    # none with a real page yet.
    path('algebra-manipulation-changing-subject-manipulating-formulae/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-manipulating-formulae'}, name='algebra_manipulation_changing_subject_manipulating_formulae'),
    path('algebra-manipulation-changing-subject-function-machine/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-function-machine'}, name='algebra_manipulation_changing_subject_function_machine'),
    path('algebra-manipulation-changing-subject-without-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-without-factorisation'}, name='algebra_manipulation_changing_subject_without_factorisation'),
    path('algebra-manipulation-changing-subject-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-changing-subject-with-factorisation'}, name='algebra_manipulation_changing_subject_with_factorisation'),

    # Түрлөндүрүү > Бир кашааны ачуу - all 7 slots, none with a real
    # page yet.
    path('algebra-manipulation-expand-single-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-without-coefficients'}, name='algebra_manipulation_expand_single_without_coefficients'),
    path('algebra-manipulation-expand-single-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-with-coefficients'}, name='algebra_manipulation_expand_single_with_coefficients'),
    path('algebra-manipulation-expand-single-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-with-indices'}, name='algebra_manipulation_expand_single_with_indices'),
    path('algebra-manipulation-expand-single-multiple/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-multiple'}, name='algebra_manipulation_expand_single_multiple'),
    path('algebra-manipulation-expand-single-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-mixed'}, name='algebra_manipulation_expand_single_mixed'),
    path('algebra-manipulation-expand-single-factorisation-without-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-factorisation-without-indices'}, name='algebra_manipulation_expand_single_factorisation_without_indices'),
    path('algebra-manipulation-expand-single-factorisation-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-single-factorisation-with-indices'}, name='algebra_manipulation_expand_single_factorisation_with_indices'),

    # Түрлөндүрүү > Эки жана үч кашааны ачуу - all 7 slots, none with a
    # real page yet.
    path('algebra-manipulation-expand-double-triple-double-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-double-without-coefficients'}, name='algebra_manipulation_expand_double_triple_double_without_coefficients'),
    path('algebra-manipulation-expand-double-triple-double-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-double-with-coefficients'}, name='algebra_manipulation_expand_double_triple_double_with_coefficients'),
    path('algebra-manipulation-expand-double-triple-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-with-factorisation'}, name='algebra_manipulation_expand_double_triple_with_factorisation'),
    path('algebra-manipulation-expand-double-triple-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-squares'}, name='algebra_manipulation_expand_double_triple_squares'),
    path('algebra-manipulation-expand-double-triple-triple/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-triple'}, name='algebra_manipulation_expand_double_triple_triple'),
    path('algebra-manipulation-expand-double-triple-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-mixed'}, name='algebra_manipulation_expand_double_triple_mixed'),
    path('algebra-manipulation-expand-double-triple-with-surds/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expand-double-triple-with-surds'}, name='algebra_manipulation_expand_double_triple_with_surds'),

    # Өзгөртүп түзүү > Бир кашаага ажыратуу - both slots, none with a
    # real page yet.
    path('algebra-manipulation-factorise-single-without-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-without-indices'}, name='algebra_manipulation_factorise_single_without_indices'),
    path('algebra-manipulation-factorise-single-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-with-indices'}, name='algebra_manipulation_factorise_single_with_indices'),

    # Өзгөртүп түзүү > Эки кашаага ажыратуу - all 7 slots, none with a
    # real page yet.
    path('algebra-manipulation-factorise-double-quadratic-without-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-quadratic-without-coefficients'}, name='algebra_manipulation_factorise_double_quadratic_without_coefficients'),
    path('algebra-manipulation-factorise-double-quadratic-with-coefficients/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-quadratic-with-coefficients'}, name='algebra_manipulation_factorise_double_quadratic_with_coefficients'),
    path('algebra-manipulation-factorise-double-with-expanding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-with-expanding'}, name='algebra_manipulation_factorise_double_with_expanding'),
    path('algebra-manipulation-factorise-double-completing-square/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-completing-square'}, name='algebra_manipulation_factorise_double_completing_square'),
    path('algebra-manipulation-factorise-double-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-difference-squares'}, name='algebra_manipulation_factorise_double_difference_squares'),
    path('algebra-manipulation-factorise-double-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-mixed'}, name='algebra_manipulation_factorise_double_mixed'),
    path('algebra-manipulation-factorise-double-grouping/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-double-grouping'}, name='algebra_manipulation_factorise_double_grouping'),

    # Өзгөртүп түзүү > Белгилөө - all 14 slots, none with a real page
    # yet.
    path('algebra-manipulation-notation-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-adding'}, name='algebra_manipulation_notation_adding'),
    path('algebra-manipulation-notation-adding-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-adding-brackets'}, name='algebra_manipulation_notation_adding_brackets'),
    path('algebra-manipulation-notation-adding-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-adding-indices'}, name='algebra_manipulation_notation_adding_indices'),
    path('algebra-manipulation-notation-multiplying/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-multiplying'}, name='algebra_manipulation_notation_multiplying'),
    path('algebra-manipulation-notation-multiplying-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-multiplying-adding'}, name='algebra_manipulation_notation_multiplying_adding'),
    path('algebra-manipulation-notation-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-dividing'}, name='algebra_manipulation_notation_dividing'),
    path('algebra-manipulation-notation-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-multiplying-dividing'}, name='algebra_manipulation_notation_multiplying_dividing'),
    path('algebra-manipulation-notation-squared-cubed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-squared-cubed'}, name='algebra_manipulation_notation_squared_cubed'),
    path('algebra-manipulation-notation-mixed-arithmetic/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-mixed-arithmetic'}, name='algebra_manipulation_notation_mixed_arithmetic'),
    path('algebra-manipulation-notation-negative-fractional-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-negative-fractional-indices'}, name='algebra_manipulation_notation_negative_fractional_indices'),
    path('algebra-manipulation-notation-rational-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-rational-with-factorisation'}, name='algebra_manipulation_notation_rational_with_factorisation'),
    path('algebra-manipulation-notation-rational-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-rational-difference-squares'}, name='algebra_manipulation_notation_rational_difference_squares'),
    path('algebra-manipulation-notation-mixed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-mixed'}, name='algebra_manipulation_notation_mixed'),
    path('algebra-manipulation-notation-mixed-all/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-notation-mixed-all'}, name='algebra_manipulation_notation_mixed_all'),

    # Өзгөртүп түзүү > Бир кашаага ажыратуу - 2 more slots found on a
    # fuller screenshot.
    path('algebra-manipulation-factorise-single-expanding-without-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-expanding-without-indices'}, name='algebra_manipulation_factorise_single_expanding_without_indices'),
    path('algebra-manipulation-factorise-single-expanding-with-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-factorise-single-expanding-with-indices'}, name='algebra_manipulation_factorise_single_expanding_with_indices'),

    # Өзгөртүп түзүү > Аралаш - both slots, none with a real page yet.
    path('algebra-manipulation-mixed-foundation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-mixed-foundation'}, name='algebra_manipulation_mixed_foundation'),
    path('algebra-manipulation-mixed-higher/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-mixed-higher'}, name='algebra_manipulation_mixed_higher'),

    # Ырааттуулуктар > Сызыктуу - all 4 slots, none with a real page yet.
    path('algebra-sequences-linear-introduction/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-introduction'}, name='algebra_sequences_linear_introduction'),
    path('algebra-sequences-linear-evaluating-terms/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-evaluating-terms'}, name='algebra_sequences_linear_evaluating_terms'),
    path('algebra-sequences-linear-from-2-terms/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-from-2-terms'}, name='algebra_sequences_linear_from_2_terms'),
    path('algebra-sequences-linear-summing/', operation_placeholder_view, {'operation_slug': 'algebra-sequences-linear-summing'}, name='algebra_sequences_linear_summing'),

    # Өзгөртүп түзүү > Туюнтмаларды жөнөкөйлөтүү - all 13 slots, none
    # with a real page yet.
    path('algebra-manipulation-expressions-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-adding'}, name='algebra_manipulation_expressions_adding'),
    path('algebra-manipulation-expressions-adding-brackets/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-adding-brackets'}, name='algebra_manipulation_expressions_adding_brackets'),
    path('algebra-manipulation-expressions-adding-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-adding-indices'}, name='algebra_manipulation_expressions_adding_indices'),
    path('algebra-manipulation-expressions-multiplying/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-multiplying'}, name='algebra_manipulation_expressions_multiplying'),
    path('algebra-manipulation-expressions-multiplying-adding/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-multiplying-adding'}, name='algebra_manipulation_expressions_multiplying_adding'),
    path('algebra-manipulation-expressions-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-dividing'}, name='algebra_manipulation_expressions_dividing'),
    path('algebra-manipulation-expressions-multiplying-dividing/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-multiplying-dividing'}, name='algebra_manipulation_expressions_multiplying_dividing'),
    path('algebra-manipulation-expressions-squared-cubed/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-squared-cubed'}, name='algebra_manipulation_expressions_squared_cubed'),
    path('algebra-manipulation-expressions-mixed-arithmetic/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-mixed-arithmetic'}, name='algebra_manipulation_expressions_mixed_arithmetic'),
    path('algebra-manipulation-expressions-negative-fractional-indices/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-negative-fractional-indices'}, name='algebra_manipulation_expressions_negative_fractional_indices'),
    path('algebra-manipulation-expressions-rational-with-factorisation/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-rational-with-factorisation'}, name='algebra_manipulation_expressions_rational_with_factorisation'),
    path('algebra-manipulation-expressions-rational-difference-squares/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-rational-difference-squares'}, name='algebra_manipulation_expressions_rational_difference_squares'),
    path('algebra-manipulation-expressions-mixed-all/', operation_placeholder_view, {'operation_slug': 'algebra-manipulation-expressions-mixed-all'}, name='algebra_manipulation_expressions_mixed_all'),

    # Геометрия > Бурчтар > Бурч фактылары - 6 slots, none with a real
    # page yet.
    path('geometry-angles-angle-facts-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-vocabulary'}, name='geometry_angles_angle_facts_vocabulary'),
    path('geometry-angles-angle-facts-around-a-point/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-around-a-point'}, name='geometry_angles_angle_facts_around_a_point'),
    path('geometry-angles-angle-facts-on-straight-lines/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-on-straight-lines'}, name='geometry_angles_angle_facts_on_straight_lines'),
    path('geometry-angles-angle-facts-vertically-opposite/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-vertically-opposite'}, name='geometry_angles_angle_facts_vertically_opposite'),
    path('geometry-angles-angle-facts-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-triangles'}, name='geometry_angles_angle_facts_triangles'),
    path('geometry-angles-angle-facts-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-angles-angle-facts-mixed'}, name='geometry_angles_angle_facts_mixed'),

    # Геометрия > Бурчтар > Чийүү жана өлчөө - 4 slots, none with a
    # real page yet.
    path('geometry-angles-drawing-measuring-drawing/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-drawing'}, name='geometry_angles_drawing_measuring_drawing'),
    path('geometry-angles-drawing-measuring-measuring/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-measuring'}, name='geometry_angles_drawing_measuring_measuring'),
    path('geometry-angles-drawing-measuring-both/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-both'}, name='geometry_angles_drawing_measuring_both'),
    path('geometry-angles-drawing-measuring-estimating/', operation_placeholder_view, {'operation_slug': 'geometry-angles-drawing-measuring-estimating'}, name='geometry_angles_drawing_measuring_estimating'),

    # Геометрия > Бурчтар > Тегерек теоремалары - 10 slots, none with a
    # real page yet.
    path('geometry-angles-circle-theorems-vocabulary/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-vocabulary'}, name='geometry_angles_circle_theorems_vocabulary'),
    path('geometry-angles-circle-theorems-alternate-segment/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-alternate-segment'}, name='geometry_angles_circle_theorems_alternate_segment'),
    path('geometry-angles-circle-theorems-at-circumference/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-at-circumference'}, name='geometry_angles_circle_theorems_at_circumference'),
    path('geometry-angles-circle-theorems-cyclic-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-cyclic-quadrilaterals'}, name='geometry_angles_circle_theorems_cyclic_quadrilaterals'),
    path('geometry-angles-circle-theorems-tangents-chords/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-tangents-chords'}, name='geometry_angles_circle_theorems_tangents_chords'),
    path('geometry-angles-circle-theorems-combined/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-combined'}, name='geometry_angles_circle_theorems_combined'),
    path('geometry-angles-circle-theorems-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-mixed'}, name='geometry_angles_circle_theorems_mixed'),
    path('geometry-angles-circle-theorems-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-with-pythagoras'}, name='geometry_angles_circle_theorems_with_pythagoras'),
    path('geometry-angles-circle-theorems-with-trigonometry/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-with-trigonometry'}, name='geometry_angles_circle_theorems_with_trigonometry'),
    path('geometry-angles-circle-theorems-intersecting-chords/', operation_placeholder_view, {'operation_slug': 'geometry-angles-circle-theorems-intersecting-chords'}, name='geometry_angles_circle_theorems_intersecting_chords'),

    # Геометрия > Бурчтар > Параллель сызыктар - 2 known slots
    # (screenshot was cut off), none with a real page yet.
    path('geometry-angles-parallel-lines-introduction/', operation_placeholder_view, {'operation_slug': 'geometry-angles-parallel-lines-introduction'}, name='geometry_angles_parallel_lines_introduction'),
    path('geometry-angles-parallel-lines-solving-equations/', operation_placeholder_view, {'operation_slug': 'geometry-angles-parallel-lines-solving-equations'}, name='geometry_angles_parallel_lines_solving_equations'),

    # Геометрия > Бурчтар > Көп бурчтуктар - 5 flat slots plus "Аралаш"
    # category's own 2 slots.
    path('geometry-angles-polygons-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-triangles'}, name='geometry_angles_polygons_triangles'),
    path('geometry-angles-polygons-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-quadrilaterals'}, name='geometry_angles_polygons_quadrilaterals'),
    path('geometry-angles-polygons-special-quadrilaterals/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-special-quadrilaterals'}, name='geometry_angles_polygons_special_quadrilaterals'),
    path('geometry-angles-polygons-regular/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-regular'}, name='geometry_angles_polygons_regular'),
    path('geometry-angles-polygons-irregular/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-irregular'}, name='geometry_angles_polygons_irregular'),
    path('geometry-angles-polygons-mixed-without-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-mixed-without-circle-theorems'}, name='geometry_angles_polygons_mixed_without_circle_theorems'),
    path('geometry-angles-polygons-mixed-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-angles-polygons-mixed-with-circle-theorems'}, name='geometry_angles_polygons_mixed_with_circle_theorems'),

    # Геометрия > Азимут - all 5 slots, none with a real page yet.
    path('geometry-bearings-cardinal-points/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-cardinal-points'}, name='geometry_bearings_cardinal_points'),
    path('geometry-bearings-measuring/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-measuring'}, name='geometry_bearings_measuring'),
    path('geometry-bearings-with-scale-drawings/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-with-scale-drawings'}, name='geometry_bearings_with_scale_drawings'),
    path('geometry-bearings-calculating/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-calculating'}, name='geometry_bearings_calculating'),
    path('geometry-bearings-with-trigonometry/', operation_placeholder_view, {'operation_slug': 'geometry-bearings-with-trigonometry'}, name='geometry_bearings_with_trigonometry'),

    # Геометрия > Координаттар - all 6 slots, none with a real page yet.
    path('geometry-coordinates-reading/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-reading'}, name='geometry_coordinates_reading'),
    path('geometry-coordinates-reading-plotting/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-reading-plotting'}, name='geometry_coordinates_reading_plotting'),
    path('geometry-coordinates-midpoint-endpoint/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-midpoint-endpoint'}, name='geometry_coordinates_midpoint_endpoint'),
    path('geometry-coordinates-line-segments-ratio/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-line-segments-ratio'}, name='geometry_coordinates_line_segments_ratio'),
    path('geometry-coordinates-geometric-problems/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-geometric-problems'}, name='geometry_coordinates_geometric_problems'),
    path('geometry-coordinates-with-pythagoras/', operation_placeholder_view, {'operation_slug': 'geometry-coordinates-with-pythagoras'}, name='geometry_coordinates_with_pythagoras'),

    # Геометрия > Пифагор - 11 flat slots, none with a real page yet.
    path('geometry-pythagoras-introduction/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-introduction'}, name='geometry_pythagoras_introduction'),
    path('geometry-pythagoras-finding-a-or-b/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-finding-a-or-b'}, name='geometry_pythagoras_finding_a_or_b'),
    path('geometry-pythagoras-finding-a-b-or-c/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-finding-a-b-or-c'}, name='geometry_pythagoras_finding_a_b_or_c'),
    path('geometry-pythagoras-isosceles-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-isosceles-triangles'}, name='geometry_pythagoras_isosceles_triangles'),
    path('geometry-pythagoras-real-life/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-real-life'}, name='geometry_pythagoras_real_life'),
    path('geometry-pythagoras-3d/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-3d'}, name='geometry_pythagoras_3d'),
    path('geometry-pythagoras-coordinates/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-coordinates'}, name='geometry_pythagoras_coordinates'),
    path('geometry-pythagoras-mixed/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-mixed'}, name='geometry_pythagoras_mixed'),
    path('geometry-pythagoras-shape-perimeters/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-shape-perimeters'}, name='geometry_pythagoras_shape_perimeters'),
    path('geometry-pythagoras-with-surds/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-with-surds'}, name='geometry_pythagoras_with_surds'),
    path('geometry-pythagoras-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-pythagoras-with-circle-theorems'}, name='geometry_pythagoras_with_circle_theorems'),

    # Геометрия > Окшоштук - all 4 slots, none with a real page yet.
    path('geometry-similarity-similar-2d-shapes/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-similar-2d-shapes'}, name='geometry_similarity_similar_2d_shapes'),
    path('geometry-similarity-similar-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-similar-triangles'}, name='geometry_similarity_similar_triangles'),
    path('geometry-similarity-congruent-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-congruent-triangles'}, name='geometry_similarity_congruent_triangles'),
    path('geometry-similarity-length-area-volume-scale-factors/', operation_placeholder_view, {'operation_slug': 'geometry-similarity-length-area-volume-scale-factors'}, name='geometry_similarity_length_area_volume_scale_factors'),

    # Геометрия > Тригонометрия - 7 flat slots, none with a real page
    # yet.
    path('geometry-trigonometry-introduction/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-introduction'}, name='geometry_trigonometry_introduction'),
    path('geometry-trigonometry-graphs/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-graphs'}, name='geometry_trigonometry_graphs'),
    path('geometry-trigonometry-choosing-a-ratio/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-choosing-a-ratio'}, name='geometry_trigonometry_choosing_a_ratio'),
    path('geometry-trigonometry-isosceles-triangles/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-isosceles-triangles'}, name='geometry_trigonometry_isosceles_triangles'),
    path('geometry-trigonometry-without-calculator/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-without-calculator'}, name='geometry_trigonometry_without_calculator'),
    path('geometry-trigonometry-with-circle-theorems/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-with-circle-theorems'}, name='geometry_trigonometry_with_circle_theorems'),
    path('geometry-trigonometry-area-rule/', operation_placeholder_view, {'operation_slug': 'geometry-trigonometry-area-rule'}, name='geometry_trigonometry_area_rule'),

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