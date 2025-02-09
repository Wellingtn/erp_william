from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='sub')
def sub(value, arg):
    return Decimal(value) - Decimal(arg)

