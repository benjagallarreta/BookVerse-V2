from django import template

register = template.Library()

@register.filter
def to(value, max_value):
    return range(value, max_value + 1)