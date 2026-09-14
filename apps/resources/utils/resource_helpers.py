from ..models import Resource


from apps.resources.models import Resource


def get_active_resources():

    resources = Resource.objects.filter(is_active=True)

    return {
        r.title: r
        for r in resources
    }


