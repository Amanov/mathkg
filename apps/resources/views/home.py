from django.shortcuts import render


def home_screen_view(request):
    return render(request, 'resources/home.html', {})


def success_view(request):

    return render(
        request,
        'resources/sandar/SuccessMessage.html',
        {}
    )