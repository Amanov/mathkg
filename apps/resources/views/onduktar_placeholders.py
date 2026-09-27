from django.http import Http404
from django.shortcuts import render

# The other 7 slots of Decimals > Arithmetic: 1 Digit (Кошуу/Adding is the
# one real hand-built page - see koshuu_1_digit_view - the rest have no
# material yet). Shares that page's exact visual chrome (see
# templates/resources/onduktar/operation_placeholder.html) so navigating
# between a real operation and a "coming soon" one feels like the same
# page family, not two different systems. Each gets its own short URL
# (config/urls.py), matching koshuu-1-digit/'s own convention, instead of
# the long generic /resources/topic/number/... path.
OPERATION_PLACEHOLDER_TITLES = {
    'subtracting-1-digit': 'Кемитүү — 1 орундуу сандар',
    'adding-subtracting-1-digit': 'Кошуу жана кемитүү — 1 орундуу сандар',
    'multiplying-1-digit': 'Көбөйтүү — 1 орундуу сандар',
    'dividing-1-digit': 'Бөлүү — 1 орундуу сандар',
    'multiplying-dividing-1-digit': 'Көбөйтүү жана бөлүү — 1 орундуу сандар',
    'mixed-1-digit': 'Аралаш эсептөөлөр — 1 орундуу сандар',
    'dividing-by-less-than-1': '1ден кичине ондукка бөлүү',
}


def operation_placeholder_view(request, operation_slug):
    try:
        page_title = OPERATION_PLACEHOLDER_TITLES[operation_slug]
    except KeyError:
        raise Http404('Unknown operation')
    return render(
        request,
        'resources/onduktar/operation_placeholder.html',
        {'page_title': page_title},
    )
