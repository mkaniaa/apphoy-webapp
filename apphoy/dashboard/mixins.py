from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

from common.models import get_field_names, get_verbose_field_names
from dashboard.views import DashboardAddView, DashboardEditView, DashboardDeleteView


class DashboardListMixin:
    dashboard_title = None
    edit_url_name = None
    add_view = DashboardAddView
    edit_view = DashboardEditView
    delete_view = DashboardDeleteView

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, exclude="ID")
        attributes = get_field_names(self.model, exclude="id")
        context = super(DashboardListMixin, self).get_context_data(**kwargs)
        context["headers"] = headers
        context["attributes"] = attributes
        context["dashboard_title"] = self.dashboard_title
        context["edit_url_name"] = self.edit_url_name

    def post(self, request, *args, **kwargs):
        try:
            if request.POST['action'] == 'Add':
                return self.add_view.as_view()(request)
            elif request.POST['action'] == 'Update':
                return self.edit_view.as_view()(request, pk=kwargs['pk'])
            else:
                return self.delete_view.as_view()(request)
        except PermissionDenied:
            return redirect(reverse('person_no_permission'))
