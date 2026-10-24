from django.shortcuts import render

from apps.resources.topic_pages import FOUR_BASIC_OPERATIONS, build_topic_page
from apps.resources.utils.resource_helpers import get_active_resources
from apps.resources.views.onduktar_placeholders import pack_or_placeholder, placeholder_page

from apps.resources.data.directed_numbers_page import DIRECTED_NUMBERS
from apps.resources.data.grade_topic_pages import (
    ALL_OPERATIONS,
    HCF_LCM_PRIME_FACTORISATION,
    INTEGERS_ADD_SUB_1_2_DIGIT,
    KOSHUU_1_DIGIT,
)


def four_basic_operations_view(request):
    page = build_topic_page(
        FOUR_BASIC_OPERATIONS, get_active_resources(), request.user,
    )
    return render(request, 'resources/topic_materials.html', {'page': page})


def directed_numbers_view(request):
    return _topic_page(request, DIRECTED_NUMBERS)


def all_operations_view(request):
    return _topic_page(request, ALL_OPERATIONS)


def _topic_page(request, spec):
    page = build_topic_page(spec, get_active_resources(), request.user)
    return render(request, 'resources/topic_materials.html', {'page': page})


def koshuu_1_digit_view(request):
    return _topic_page(request, KOSHUU_1_DIGIT)


def integers_adding_subtracting_1_2_digit_view(request):
    return _topic_page(request, INTEGERS_ADD_SUB_1_2_DIGIT)


def hcf_lcm_prime_factorisation_mixed_view(request):
    return _topic_page(request, HCF_LCM_PRIME_FACTORISATION)


def subtracting_1_digit_view(request):
    return placeholder_page(request, 'Кемитүү — 1 орундуу сандар')


def adding_subtracting_1_digit_view(request):
    return placeholder_page(request, 'Кошуу жана кемитүү — 1 орундуу сандар')


def algebra_linear_var1side_noncalc_1step_view(request):
    return pack_or_placeholder(request, 'algebra-linear-var1side-noncalc-1step', 'Белгисиз бир жагында: 1-кадам')
