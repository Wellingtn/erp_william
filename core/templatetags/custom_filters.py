from django import template

register = template.Library()

@register.filter(name='abs')
def abs_filter(value):
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return value  # Return the original value if it can't be converted to a number

