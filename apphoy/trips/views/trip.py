from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
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
    manage_view_obj = None


class TripAddView(ManageTripMixin, CreateView):
    fields = None  # Specifying both "fields" and "form_class" is not permitted.
    permission_required = "trips.add_trip"
    form_class = TripManageForm
    template_name = "base/dashboard_base.html"  # Must be specified in case of invalid form.

    def form_invalid(self, form):
        """
        Method must be overwritten to get context from the main list view.
        """
        self.manage_view_obj.form = form
        context = self.manage_view_obj.get_context_data()
        return self.render_to_response(context)


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

    def has_permission(self):
        return True if self.request.method == "GET" else super(TripEditView, self).has_permission()

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, "You have no permission for this action!")
            return HttpResponseRedirect(self.request.path_info)

        return super(TripEditView, self).handle_no_permission()


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

    def render_edit_view(self, request, **kwargs):
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
