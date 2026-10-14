from django.shortcuts import render

from apps.resources.topic_pages import CALCULATOR_FRACTIONS, build_topic_page
from apps.resources.utils.resource_helpers import get_active_resources

# Сандар > Калькулятор колдонуу > Калькулятордо бөлчөктөр. Built on the
# same topic_materials.html template as to_fractions_view, following the
# screenshot reference the user supplied (Worksheets / Activities /
# Teacher-Led Activities sections). The MenuItem for this page has its
# subtopic/subsubtopic FKs cleared and url_name set to 'calculator_fractions'
# so it resolves here instead of the old empty generic Topic/SubSubtopic
# page (see fix_calculator_fractions_menu_link.py).


def calculator_fractions_view(request):
    page = build_topic_page(CALCULATOR_FRACTIONS, get_active_resources(), request.user)
    return render(request, 'resources/topic_materials.html', {'page': page})
