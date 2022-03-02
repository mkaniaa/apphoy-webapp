from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import View

from common.models import get_field_names
from dashboard.mixins import DashboardListMixin, ManageDashboardMixin, DashboardEditMixin, DashboardDeleteMixin
from ..forms.trip import TripManageForm
from ..models import Trip


class ManageTripMixin(ManageDashboardMixin):
    model = Trip
    main_list_url_name = "trip_list"
    fields = get_field_names(model, exclude=["id", "stages"])


class TripAddView(ManageTripMixin, CreateView):
    fields = None  # Specifying both "fields" and "form_class" is not permitted.
    permission_required = "trips.add_trip"
    form_class = TripManageForm


class TripEditView(
    ManageTripMixin,
    DashboardEditMixin,
    SuccessMessageMixin,
    UpdateView
):
    permission_required = "trips.change_trip"
    template_name = "trips/trip_edit.html"
    pk_url_name = "trip_pk"
    success_message = "Trip changes saved!"

    def get_success_url(self):
        return reverse_lazy(
            "trip_edit",
            kwargs={self.pk_url_name: self.kwargs.get(self.pk_url_name)}
        )


class TripDeleteView(ManageTripMixin, DashboardDeleteMixin, View):
    permission_required = "trips.delete_trip"


class TripManageView(DashboardListMixin, LoginRequiredMixin, ListView):
    model = Trip
    dashboard_title = "Trips"
    main_url_name = "trip_list"
    edit_url_name = "trip_edit"
    exclude_fields = ["id", "slug", "stages"]
    form = TripManageForm
    pk_url_name = "trip_pk"

    def render_edit_view(self, request, kwargs):
        return self.get_edit_view().as_view()(
            request,
            trip_pk=kwargs[self.pk_url_name],
        )

    def get_add_view(self):
        return TripAddView

    def get_edit_view(self):
        return TripEditView

    def get_delete_view(self):
        return TripDeleteView
