from django.shortcuts import render

from apps.resources.models import Resource

from apps.resources.data.all_operations_data import (
    ALL_OPERATIONS_SECTIONS
)


def all_operations_view(request):

    resources = Resource.objects.filter(
        is_active=True
    )

    res = {
        r.title: r
        for r in resources
    }

    return render(
        request,
        'resources/sandar/all_operations.html',
        {
            'res': res,
            'sections': ALL_OPERATIONS_SECTIONS,
        }
    )
# from django.shortcuts import render

# from .utils.resource_helpers import (
#     get_active_resources
# )

# from .data.four_basic_operations_data import (
#     FOUR_BASIC_OPERATIONS_SECTIONS
# )


from django.shortcuts import render

from apps.resources.models import Resource



import os
from django.shortcuts import render

from apps.resources.models import Resource

from apps.resources.utils.resource_helpers import (
    get_active_resources
)


from apps.resources.data.four_basic_operations_data import (
    FOUR_BASIC_OPERATIONS_SECTIONS
)

def four_basic_operations_view(request):

    resources = Resource.objects.filter(
        is_active=True
    )

    res = {
        r.title: r
        for r in resources
    }

    return render(
        request,
        'resources/sandar/four_basic_operations.html',
        {
            'res': res,
            'sections': FOUR_BASIC_OPERATIONS_SECTIONS,
        }
    )

from apps.resources.data.directed_numbers_data import (
    DIRECTED_NUMBERS_SECTIONS
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


from ..data.all_operations_data import (
    ALL_OPERATIONS_SECTIONS
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





# def onedigitarithmetics_view(request):

#     resources = Resource.objects.filter(
#         is_active=True
#     )

#     res = {
#         r.title: r
#         for r in resources
#     }

#     return render(
#         request,
#         'resources/onduktar/onedigitarithmetics.html',
#         {
#             'res': res,
#         }
#     )

from apps.resources.data.koshuu_1_digit_data import KOSHUU_1_DIGIT_SECTIONS

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
