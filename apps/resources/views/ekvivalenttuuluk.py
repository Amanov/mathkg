import copy

from django.shortcuts import render

from apps.resources.data.pack_pages import FDP, FDPR
from apps.resources.topic_pages import build_topic_page
from apps.resources.utils.resource_helpers import get_active_resources
from apps.resources.views.onduktar_placeholders import placeholder_page

# The pages under Ондуктар > Эквиваленттүүлүк. Their old files were built on
# goteachmaths templates, so the owner had them taken off the site
# (2026-10-24, migration 0033 hides the rows). They now carry our own 6-класс
# fraction/decimal/percent pack (and the ratio pack on the FDPR page);
# recurring decimals stay a placeholder because the pack does not teach
# them. The old templates in templates/resources/ekvivalenttuuluk/ and the
# TO_FRACTIONS spec are kept for reference only.


def _pack_page(request, spec, page_title):
    spec = copy.copy(spec)
    spec['crumb'] = f"{spec['crumb']} › {page_title}"
    page = build_topic_page(spec, get_active_resources(), request.user)
    return render(request, 'resources/topic_materials.html', {'page': page})


def to_fractions_view(request):
    return _pack_page(request, FDP, 'Ондуктарды бөлчөккө айландыруу')


def to_percentages_view(request):
    return _pack_page(request, FDP, 'Ондуктарды пайыздарга айландыруу')


def to_both_view(request):
    return _pack_page(request, FDP, 'Ондуктарды бөлчөккө жана пайызга айландыруу')


def recurring_decimals_to_fractions_view(request):
    return placeholder_page(request, 'Кайталануучу ондуктарды бөлчөккө айландыруу')


def with_fractions_view(request):
    return _pack_page(request, FDP, 'Бөлчөктөрдү жана ондуктарды бири-бирине айландыруу')


def with_percentages_view(request):
    return _pack_page(request, FDP, 'Бөлчөктөрдү жана пайыздарды бири-бирине айландыруу')


def fdp_view(request):
    return _pack_page(request, FDP, 'Бөлчөк, ондук жана пайыздык эквиваленттүүлүк')


def fdp_ordering_view(request):
    return _pack_page(request, FDP, 'Бөлчөктөрдү, ондуктарды жана пайыздарды ирээттөө')


def fdpr_view(request):
    return _pack_page(request, FDPR, 'Бөлчөк, ондук, пайыз жана катыштын эквиваленттүүлүгү')
