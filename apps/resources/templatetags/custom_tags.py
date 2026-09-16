from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def safe_url(url_name):
    """
    Reverse a URL name the way {% url %} does, but degrade to '#' instead
    of raising NoReverseMatch. MenuItem.url_name is free-text data entered
    through the admin; the menu itself renders via a context processor on
    every single page, so one MenuItem pointing at a URL name that needs
    arguments (or that no longer exists) would otherwise 500 the entire
    site rather than just that one link.
    """
    if not url_name:
        return '#'
    try:
        return reverse(url_name)
    except NoReverseMatch:
        return '#'