from django import template

register = template.Library()


@register.simple_tag
def attribute_value(obj, attr_name):
    """
    Returns attribute value of the object if exists any with the name given as a string.
    """
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None

