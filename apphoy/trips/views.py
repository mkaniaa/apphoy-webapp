from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateResponseMixin

from apphoy.models import get_field_names
from .models import Trip, TripStage


class TripStageListView(TemplateResponseMixin, View):
    model = TripStage
    template_name = 'trips/list.html'

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


class ManageTripMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Trip
    fields = get_field_names(model, exclude=['id'])
    success_url = reverse_lazy('trip_list')


class TripAddView(ManageTripMixin, CreateView):
    template_name = 'trips/manage/trip/form.html'
    permission_required = 'trip.add_trip'


class TripEditView(ManageTripMixin, UpdateView):
    template_name = 'trips/manage/trip/form.html'
    permission_required = 'trip.change_trip'


class TripDeleteView(View):
    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        trip.delete()
        return redirect('trip_list')
