from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from common.models import get_field_names, get_verbose_field_names
from .forms import TripCreateForm
from .models import Trip, TripStage


class TripManageView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/dashboard_trips.html'

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, exclude=['ID', 'slug'])
        attributes = get_field_names(self.model, exclude=['id', 'slug'])
        context = super(TripManageView, self).get_context_data(**kwargs)
        context['headers'] = headers
        context['attributes'] = attributes

        return context


class ManageTripMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Trip
    fields = get_field_names(model, exclude=['id', 'stages'])
    success_url = reverse_lazy('trip_list')


class TripEditView(ManageTripMixin, UpdateView):
    template_name = 'trips/manage/trip/form.html'
    permission_required = 'trip.change_trip'


class TripDeleteView(View):
    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        trip.delete()
        return redirect('trip_list')
