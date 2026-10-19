from django.shortcuts import render

from apps.resources.models import Resource

from apps.resources.topic_pages import FOUR_BASIC_OPERATIONS, build_topic_page
from apps.resources.utils.resource_helpers import get_active_resources

from apps.resources.data.all_operations_data import ALL_OPERATIONS_SECTIONS
from apps.resources.data.directed_numbers_page import directed_numbers_spec
from apps.resources.data.grade_topic_pages import (
    HCF_LCM_PRIME_FACTORISATION,
    INTEGERS_ADD_SUB_1_2_DIGIT,
    KOSHUU_1_DIGIT,
)
from apps.resources.data.subtracting_1_digit_data import SUBTRACTING_1_DIGIT_SECTIONS
from apps.resources.data.adding_subtracting_1_digit_data import ADDING_SUBTRACTING_1_DIGIT_SECTIONS
from apps.resources.data.algebra_linear_data import ALGEBRA_LINEAR_VAR1SIDE_NONCALC_1STEP_SECTIONS


def four_basic_operations_view(request):
    page = build_topic_page(
        FOUR_BASIC_OPERATIONS, get_active_resources(), request.user,
    )
    return render(request, 'resources/topic_materials.html', {'page': page})


def directed_numbers_view(request):
    resources = get_active_resources()
    older = Resource.objects.filter(
        is_active=True,
        subsubtopic__title='Эсептөөлөр',
        subsubtopic__subtopic__title='Багытталган сандар',
    ).values_list('title', flat=True)
    page = build_topic_page(directed_numbers_spec(older), resources, request.user)
    return render(request, 'resources/topic_materials.html', {'page': page})


def all_operations_view(request):
    return render(
        request,
        'resources/sandar/all_operations.html',
        {
            'res': get_active_resources(),
            'sections': ALL_OPERATIONS_SECTIONS,
        }
    )


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
    return render(
        request,
        'resources/onduktar/subtracting_1_digit.html',
        {
            'res': get_active_resources(),
            'sections': SUBTRACTING_1_DIGIT_SECTIONS,
            'page_title': 'Кемитүү — 1 орундуу сандар',
        }
    )


def adding_subtracting_1_digit_view(request):
    return render(
        request,
        'resources/onduktar/adding_subtracting_1_digit.html',
        {
            'res': get_active_resources(),
            'sections': ADDING_SUBTRACTING_1_DIGIT_SECTIONS,
            'page_title': 'Кошуу жана кемитүү — 1 орундуу сандар',
        }
    )


def algebra_linear_var1side_noncalc_1step_view(request):
    return render(
        request,
        'resources/algebra/linear_var1side_noncalc_1step.html',
        {
            'res': get_active_resources(),
            'sections': ALGEBRA_LINEAR_VAR1SIDE_NONCALC_1STEP_SECTIONS,
            'page_title': 'Белгисиз бир жагында: 1-кадам',
        }
    )
