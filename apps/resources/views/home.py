from django.shortcuts import render

from apps.account.models import Account


def home_screen_view(request):

    context = {}

    accounts = Account.objects.all()

    context['accounts'] = accounts

    return render(
        request,
        'resources/home.html',
        context
    )


def success_view(request):

    return render(
        request,
        'personal/sandar/SuccessMessage.html',
        {}
    )