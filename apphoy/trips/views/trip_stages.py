from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import View

from common.models import get_verbose_field_names, get_field_names
from trips.forms.trip_stage import TripStageManageForm
from trips.models import TripStage


class TripStagesManageView(LoginRequiredMixin, ListView):
    model = TripStage
    template_name = 'trips/trip_stages.html'
    pk = None

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, exclude=['ID', 'slug'])
        attributes = get_field_names(self.model, exclude=['id', 'slug', 'stages'])
        context = super(TripStagesManageView, self).get_context_data(**kwargs)
        context['headers'] = headers
        context['attributes'] = attributes
        context['target'] = self.pk

        if self.pk:
            trip = get_object_or_404(self.model, pk=self.pk)
            context['form'] = TripStageManageForm(instance=trip)
        else:
            context['form'] = TripStageManageForm

        return context

    def get(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        return super(TripStagesManageView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if request.POST['action'] == 'Add':
                return TripAddView.as_view()(request)
            elif request.POST['action'] == 'Update':
                return TripEditView.as_view()(request, pk=kwargs['pk'])
            else:
                return TripStagesDeleteView.as_view()(request)
        except PermissionDenied:
            return redirect(reverse('trip_no_permission'))


class TripStagesManageNoPermissionView(TripStagesManageView):
    template_name = 'trips/dashboard_trips_no_permission.html'


class ManageTripStagesMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = TripStage
    success_url = reverse_lazy('trip_stages')
    raise_exception = True


class TripStagesDeleteView(ManageTripStagesMixin, View):
    permission_required = 'trips.delete_trip'

    def post(self, request, *args, **kwargs):
        trip_ids = request.POST.getlist('ids[]')
        for trip_id in trip_ids:
            trip = get_object_or_404(TripStage, id=trip_id)
            trip.delete()
        return redirect(reverse('trip_list'))


class TripAddView(ManageTripStagesMixin, CreateView):
    model = TripStage
    success_url = reverse_lazy('trip_list')
    permission_required = 'trips.add_trip'
    form_class = TripStageManageForm

    def get_form_kwargs(self):
        kwargs = super(TripAddView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs


class TripEditView(ManageTripStagesMixin, UpdateView):
    model = TripStage
    permission_required = 'trips.change_trip'
    fields = get_field_names(model, exclude=['id', 'stages'])

    def get_object(self, queryset=None):
        return TripStage.objects.get(pk=self.kwargs.get("pk"))
