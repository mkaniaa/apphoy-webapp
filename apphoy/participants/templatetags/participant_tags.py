from django import template

register = template.Library()


@register.simple_tag
def attribute_value(obj, attr_name):
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None
