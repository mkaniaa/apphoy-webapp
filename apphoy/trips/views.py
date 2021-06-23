from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateResponseMixin

from apphoy.models import get_field_names
from .forms import TripCreateForm
from .models import Trip, TripStage


class TripListView(CreateView):
    model = Trip
    template_name = 'trips/list.html'
    form_class = TripCreateForm
    success_url = '/trips/'

    def get_context_data(self, trip_slug=None, **kwargs):
        if trip_slug is None:
            first_trip = Trip.objects.first()
            if first_trip:
                trip_slug = first_trip.slug
                trip = get_object_or_404(Trip, slug=trip_slug)
            else:
                trip = None
        else:
            trip = get_object_or_404(Trip, slug=trip_slug)

        trips = Trip.objects.all()
        trip_stages = TripStage.objects.filter(trip=trip)

        context = super(TripListView, self).get_context_data(**kwargs)
        context['trips'] = trips
        context['trip'] = trip
        context['trip_stages'] = trip_stages

        return context


class ManageTripMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Trip
    fields = get_field_names(model, exclude=['id', 'stages'])
    success_url = reverse_lazy('trip_list')


class TripAddView(ManageTripMixin, CreateView):
    permission_required = 'trip.add_trip'


class TripEditView(ManageTripMixin, UpdateView):
    template_name = 'trips/manage/trip/form.html'
    permission_required = 'trip.change_trip'


class TripDeleteView(View):
    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        trip.delete()
        return redirect('trip_list')
