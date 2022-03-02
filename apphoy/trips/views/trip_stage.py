from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import View

from common.models import get_field_names
from dashboard.mixins import ManageDashboardMixin, DashboardEditMixin, DashboardDeleteMixin, DashboardListMixin
from trips.forms.trip_stage import TripStageManageForm
from trips.models import TripStage


class ManageTripStageMixin(ManageDashboardMixin):
    model = TripStage
    template_name = "trips/trip_stage.html"
    fields = get_field_names(model, exclude=["id", "trip"])
    
    def get_success_url(self):
        print(self.kwargs)
        return reverse_lazy(
            "trip_stage_list",
            kwargs={"trip_pk": self.kwargs["trip_pk"]}
        )


class TripStageAddView(ManageTripStageMixin, CreateView):
    fields = None  # Specifying both "fields" and "form_class" is not permitted.
    permission_required = "trips.add_tripstage"
    form_class = TripStageManageForm

    def get_initial(self):
        initial = super().get_initial()
        initial["trip_pk"] = self.kwargs.get("trip_pk")
        print(f"kwargs: {self.kwargs}")
        print(f"ustawiam initial: {initial['trip_pk']}")
        return initial


class TripStageEditView(ManageTripStageMixin, DashboardEditMixin, UpdateView):
    permission_required = "trips.change_tripstage"
    pk_url_name = "trip_stage_pk"


class TripStageDeleteView(ManageTripStageMixin, DashboardDeleteMixin, View):
    permission_required = "trips.delete_tripstage"
    

class TripStageManageView(DashboardListMixin, LoginRequiredMixin, ListView):
    model = TripStage
    main_url_name = "trip_stage_list"
    edit_url_name = "trip_stage_edit"
    exclude_fields = ["id", "slug", "trip"]
    form = TripStageManageForm
    template_name = "trips/trip_stage.html"
    trip_stage_pk = None
    pk_url_name = "trip_stage_pk"

    def get_context_data(self, **kwargs):
        context = super(TripStageManageView, self).get_context_data(**kwargs)
        context["target"] = self.trip_stage_pk

        if self.trip_stage_pk:
            trip_stage = get_object_or_404(self.model, pk=self.trip_stage_pk)
            context["form"] = self.form(instance=trip_stage)
        else:
            context["form"] = self.form

        return context

    def get(self, request, *args, **kwargs):
        self.trip_stage_pk = kwargs.get(self.pk_url_name)
        return super(TripStageManageView, self).get(request, *args, **kwargs)

    def render_add_view(self, request, kwargs):
        return self.get_add_view().as_view()(
            request,
            trip_pk=self.kwargs.get("trip_pk")
        )

    def render_edit_view(self, request, kwargs):
        return self.get_edit_view().as_view()(
            request,
            trip_pk=kwargs["trip_pk"],
            trip_stage_pk=kwargs["trip_stage_pk"],
        )

    def render_delete_view(self, request, kwargs):
        return self.get_delete_view().as_view()(
            request,
            trip_pk=self.kwargs.get("trip_pk")
        )

    def get_add_view(self):
        return TripStageAddView

    def get_edit_view(self):
        return TripStageEditView

    def get_delete_view(self):
        return TripStageDeleteView
