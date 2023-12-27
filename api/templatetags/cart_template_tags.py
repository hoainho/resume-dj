# from django import template
# register = template.Library()
from django.template.defaulttags import register
@register.filter
def open_navbar(is_open):
    return not is_open