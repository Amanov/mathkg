from django.shortcuts import render

from ..models import NewsPost


def news_list_view(request):
    posts = NewsPost.objects.all()
    return render(request, 'resources/news_list.html', {'posts': posts})


def about_view(request):
    return render(request, 'resources/about.html')
