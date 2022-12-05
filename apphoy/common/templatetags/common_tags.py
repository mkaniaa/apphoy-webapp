from django import template

register = template.Library()


@register.simple_tag
def attribute_value(obj, attr_name):
    """
    Returns attribute value of the object if exists any with the name given as a string.
    """
    try:
        attr_name = attr_name.lstrip("_")
        return getattr(obj, attr_name)
    except AttributeError:
        return None


@register.simple_tag
def not_in_list(val, string_list):
    """
    Checks if the value is in the list given as a string with comma-separated elements.
    """
    values = string_list.split(",")
    return True if val not in values else False

