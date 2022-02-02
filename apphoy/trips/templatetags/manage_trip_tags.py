from django import template
from django.shortcuts import get_object_or_404

from trips.models import Trip

register = template.Library()


@register.simple_tag
def trip_name(trip_id):
    """
    Returns name of the trip with given id.
    """
    return get_object_or_404(Trip, pk=trip_id).name
