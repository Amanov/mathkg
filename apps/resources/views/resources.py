from django.core.paginator import Paginator
from django.shortcuts import render

from apps.resources.models import Resource


def resources_view(request):

    category = request.GET.get('category')

    resources = Resource.objects.filter(
        is_active=True
    )

    if category:
        resources = resources.filter(
            category=category
        )

    paginator = Paginator(resources, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'resources': page_obj.object_list,
        'categories': Resource.CATEGORY_CHOICES,
        'selected_category': category,
    }

    return render(
        request,
        'resources/resources.html',
        context
    )
