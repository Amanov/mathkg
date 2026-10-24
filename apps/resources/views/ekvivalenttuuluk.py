from apps.resources.views.onduktar_placeholders import placeholder_page

# The pages under Ондуктар > Эквиваленттүүлүк. Their files were built on
# goteachmaths templates, so the owner had them taken off the site
# (2026-10-24, migration 0033 hides the rows). Each page shows the
# «даярдалууда» placeholder until our own fraction/decimal/percent pack
# replaces it. The old templates in templates/resources/ekvivalenttuuluk/
# and the TO_FRACTIONS spec are kept for reference only.


def to_fractions_view(request):
    return placeholder_page(request, 'Ондуктарды бөлчөккө айландыруу')


def to_percentages_view(request):
    return placeholder_page(request, 'Ондуктарды пайыздарга айландыруу')


def to_both_view(request):
    return placeholder_page(request, 'Ондуктарды бөлчөккө жана пайызга айландыруу')


def recurring_decimals_to_fractions_view(request):
    return placeholder_page(request, 'Кайталануучу ондуктарды бөлчөккө айландыруу')


def with_fractions_view(request):
    return placeholder_page(request, 'Бөлчөктөрдү жана ондуктарды бири-бирине айландыруу')


def with_percentages_view(request):
    return placeholder_page(request, 'Бөлчөктөрдү жана пайыздарды бири-бирине айландыруу')


def fdp_view(request):
    return placeholder_page(request, 'Бөлчөк, ондук жана пайыздык эквиваленттүүлүк')


def fdp_ordering_view(request):
    return placeholder_page(request, 'Бөлчөктөрдү, ондуктарды жана пайыздарды ирээттөө')


def fdpr_view(request):
    return placeholder_page(request, 'Бөлчөк, ондук, пайыз жана катыштын эквиваленттүүлүгү')
