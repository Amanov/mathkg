from django.shortcuts import render

from ..models import MenuItem, NewsPost


def news_list_view(request):
    posts = NewsPost.objects.all()
    return render(request, 'resources/news_list.html', {'posts': posts})


def about_view(request):
    return render(request, 'resources/about.html')


def topics_tree_view(request):
    """The full menu hierarchy as one navigable page, for a visitor who
    wants to see/search the whole curriculum at once rather than click
    through the header menu level by level."""
    roots = MenuItem.objects.filter(parent__isnull=True).prefetch_related(
        'children',
        'children__children',
        'children__children__children',
        'children__children__children__children',
        'children__children__children__children__children',
    ).order_by('order')
    return render(request, 'resources/topics_tree.html', {'roots': roots})
