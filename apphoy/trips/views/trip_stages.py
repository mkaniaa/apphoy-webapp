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
    trip_stage_pk = None

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, exclude=['ID', 'slug'])
        attributes = get_field_names(self.model, exclude=['id', 'slug', 'stages'])
        context = super(TripStagesManageView, self).get_context_data(**kwargs)
        context['headers'] = headers
        context['attributes'] = attributes
        context['target'] = self.trip_stage_pk

        if self.trip_stage_pk:
            trip_stage = get_object_or_404(self.model, pk=self.trip_stage_pk)
            context['form'] = TripStageManageForm(instance=trip_stage)
        else:
            context['form'] = TripStageManageForm

        return context

    def get(self, request, *args, **kwargs):
        self.trip_stage_pk = kwargs.get('trip_stage_pk')
        return super(TripStagesManageView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if request.POST['action'] == 'Add':
                return TripStagesAddView.as_view()(request, trip_pk=self.kwargs.get("trip_pk"))
            elif request.POST['action'] == 'Update':
                return TripStagesEditView.as_view()(request,
                                                    trip_stage_pk=kwargs['trip_stage_pk'],
                                                    trip_pk=self.kwargs.get("trip_pk"))
            else:
                return TripStagesDeleteView.as_view()(request)
        except PermissionDenied:
            return redirect(reverse('trip_no_permission'))


class TripStagesManageNoPermissionView(TripStagesManageView):
    template_name = 'trips/dashboard_trips_no_permission.html'


class ManageTripStagesMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = TripStage
    raise_exception = True
    template_name = 'trips/trip_stages.html'

    def get_success_url(self):
        return reverse_lazy('trip_stages', kwargs={"trip_pk": self.kwargs.get("trip_pk")})


class TripStagesDeleteView(ManageTripStagesMixin, View):
    permission_required = 'trips.delete_tripstage'

    def post(self, request, *args, **kwargs):
        trip_ids = request.POST.getlist('ids[]')
        for trip_id in trip_ids:
            trip = get_object_or_404(TripStage, id=trip_id)
            trip.delete()
        return redirect(reverse('trip_list'))


class TripStagesAddView(ManageTripStagesMixin, CreateView):
    model = TripStage
    permission_required = 'trips.add_tripstage'
    form_class = TripStageManageForm

    def get_initial(self):
        initial = super().get_initial()
        initial["trip_pk"] = self.kwargs.get("trip_pk")
        return initial


class TripStagesEditView(ManageTripStagesMixin, UpdateView):
    model = TripStage
    permission_required = 'trips.change_tripstage'
    fields = get_field_names(model, exclude=['id', 'stages'])

    def get_object(self, queryset=None):
        return TripStage.objects.get(pk=self.kwargs.get("trip_stage_pk"))
