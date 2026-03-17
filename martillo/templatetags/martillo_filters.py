from django import template

register = template.Library()

@register.filter(name='clp')
def clp(value):
    if value is None:
        return "0"
    try:
        # Convert to float to handle decimals if any, then to int-like formatting
        # We use a fixed Python formatting that we control
        # Format with comma as thousands separator, then replace with dot
        return "{:,.0f}".format(float(value)).replace(",", ".")
    except (ValueError, TypeError):
        return value
