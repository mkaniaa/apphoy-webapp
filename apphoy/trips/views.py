from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View

from .models import Trip, TripStage


class TripStageListView(TemplateResponseMixin, View):
    model = TripStage
    template_name = 'trips/trip_stages/list.html'

    def get(self, request, trip_slug=None):
        if trip_slug is None:
            first_trip = TripStage.objects.first()
            if first_trip:
                trip_slug = first_trip.slug
                trip = get_object_or_404(Trip, slug=trip_slug)
            else:
                trip = None
        else:
            trip = get_object_or_404(Trip, slug=trip_slug)

        trips = Trip.objects.annotate(total_stages=Count('stages'))
        trip_stages = TripStage.objects.filter(trip=trip)

        return self.render_to_response({'trips': trips,
                                        'trip': trip,
                                        'trip_stages': trip_stages})
