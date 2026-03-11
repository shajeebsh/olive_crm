from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def currency(value, symbol="$"):
    try:
        if value is None:
            return f"{symbol}0.00"
        return f"{symbol}{intcomma('{:.2f}'.format(float(value)))}"
    except (ValueError, TypeError):
        return value
