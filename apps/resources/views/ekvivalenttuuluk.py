from django.shortcuts import render

from apps.resources.utils.resource_helpers import get_active_resources

# The 9 real hand-built pages under Ондуктар > Эквиваленттүүлүк (see
# templates/resources/ekvivalenttuuluk/). These predate the site's current
# download system: each button used to call a `download_file` URL that no
# longer exists, so the templates were rewritten to use the same
# `res|get_item:'filename'` + `download_resource` pattern already used by
# other real pages (e.g. templates/resources/sandar/directed_numbers.html).
# The backing files were already sitting in media/resources/files/ - only
# the Resource DB rows needed creating (see: python manage.py
# import_resources) and the templates needed rewiring.


def to_fractions_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Bolchoktorgo_Ekvivalenttuluk.html',
        {'res': get_active_resources()},
    )


def to_percentages_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Payizga_Ekvivalenttuluk.html',
        {'res': get_active_resources()},
    )


def to_both_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Payizga_Jana_Bolchoktorgo_Ekvivalenttuluk.html',
        {'res': get_active_resources()},
    )


def recurring_decimals_to_fractions_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Kaytalanuuchu_Onduktar_Ekvivalenttuluk.html',
        {'res': get_active_resources()},
    )


def with_fractions_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Onduktardy_Jana_Bolchoktordu_BirBirineAylandyruu.html',
        {'res': get_active_resources()},
    )


def with_percentages_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Onduktardy_Jana_Payizdardy_BirBirineAylandyruu.html',
        {'res': get_active_resources()},
    )


def fdp_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Bolchok_Onduk_Payiz.html',
        {'res': get_active_resources()},
    )


def fdp_ordering_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Bolchok_Onduk_Payiz_Ireettoo.html',
        {'res': get_active_resources()},
    )


def fdpr_view(request):
    return render(
        request,
        'resources/ekvivalenttuuluk/Bolchok_Obduk_Payiz_Katyw.html',
        {'res': get_active_resources()},
    )
