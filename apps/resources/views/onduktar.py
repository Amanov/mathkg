from django.shortcuts import render

from apps.resources.models import Resource


def onedigitarithmetics_view(request):

    resources = Resource.objects.filter(
        is_active=True
    )

    res = {
        r.title: r
        for r in resources
    }

    return render(
        request,
        'resources/onduktar/onedigitarithmetics.html',
        {
            'res': res,
        }
    )