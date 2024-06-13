from django import template
import re

register = template.Library()


@register.filter(name='css_filename')
def css_filename(value):
    return re.sub(r'\s+', '_', value.lower())


@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    return None
