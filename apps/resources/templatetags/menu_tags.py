# from django import template

# register = template.Library()

# @register.inclusion_tag(
#     'partials/menu_node.html'
# )
# def render_menu(nodes):
#     return {
#         'nodes': nodes
#     }

# update 

from django import template

register = template.Library()

@register.inclusion_tag('partials/menu_node.html')
def render_menu(nodes):
    return {
        'nodes': nodes,
        'parent': False # <-- Ensures your top level items know they are parents!
    }