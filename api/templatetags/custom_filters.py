from django import template

register = template.Library()

@register.filter
def open_navbar(is_open):
    return not is_open