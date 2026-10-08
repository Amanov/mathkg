from django.shortcuts import render

from apps.resources.utils.resource_helpers import get_active_resources

from apps.resources.data.all_operations_data import ALL_OPERATIONS_SECTIONS
from apps.resources.data.four_basic_operations_data import FOUR_BASIC_OPERATIONS_SECTIONS
from apps.resources.data.directed_numbers_data import DIRECTED_NUMBERS_SECTIONS
from apps.resources.data.koshuu_1_digit_data import KOSHUU_1_DIGIT_SECTIONS
from apps.resources.data.subtracting_1_digit_data import SUBTRACTING_1_DIGIT_SECTIONS
from apps.resources.data.adding_subtracting_1_digit_data import ADDING_SUBTRACTING_1_DIGIT_SECTIONS
from apps.resources.data.algebra_linear_data import ALGEBRA_LINEAR_VAR1SIDE_NONCALC_1STEP_SECTIONS


def four_basic_operations_view(request):
    return render(
        request,
        'resources/sandar/four_basic_operations.html',
        {
            'res': get_active_resources(),
            'sections': FOUR_BASIC_OPERATIONS_SECTIONS,
        }
    )


def directed_numbers_view(request):
    return render(
        request,
        'resources/sandar/directed_numbers.html',
        {
            'res': get_active_resources(),
            'sections': DIRECTED_NUMBERS_SECTIONS,
        }
    )


def all_operations_view(request):
    return render(
        request,
        'resources/sandar/all_operations.html',
        {
            'res': get_active_resources(),
            'sections': ALL_OPERATIONS_SECTIONS,
        }
    )


def koshuu_1_digit_view(request):
    return render(
        request,
        'resources/onduktar/koshuu_1_digit.html',
        {
            'res': get_active_resources(),
            'sections': KOSHUU_1_DIGIT_SECTIONS,
            'page_title': 'Кошуу — 1 орундуу сандар',
        }
    )


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
