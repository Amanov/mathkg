from apps.resources.views.onduktar_placeholders import placeholder_page


def onedigitarithmetics_view(request):
    """The old hand-written page had no working file links.

    It now uses the shared topic layout, same as the other empty slots.
    """
    return placeholder_page(request, '1 орундук сандар менен көнүгүүлөр')