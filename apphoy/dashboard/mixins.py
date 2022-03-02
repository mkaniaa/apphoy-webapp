from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from common.models import get_field_names, get_verbose_field_names


class DashboardListMixin:
    dashboard_title = None
    main_url_name = None
    edit_url_name = None
    exclude_fields = ["id"]
    form = None
    template_name = "base/dashboard_base.html"
    pk_url_name = "pk"

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, exclude=self.exclude_fields)
        attributes = get_field_names(self.model, exclude=self.exclude_fields)
        context = super(DashboardListMixin, self).get_context_data(**kwargs)
        context["headers"] = headers
        context["attributes"] = attributes
        context["dashboard_title"] = self.dashboard_title
        context["main_url_name"] = self.main_url_name
        context["edit_url_name"] = self.edit_url_name
        context["form"] = self.form

        return context

    def post(self, request, *args, **kwargs):
        try:
            if request.POST["action"] == "Add":
                return self.render_add_view(request, kwargs)
            elif request.POST["action"] == "Update":
                return self.render_edit_view(request, kwargs)
            else:
                return self.render_delete_view(request, kwargs)
        except PermissionDenied:
            return redirect(reverse("no_permission"))

    def render_add_view(self, request, kwargs):
        return self.get_add_view().as_view()(request)

    def render_edit_view(self, request, kwargs):
        return self.get_edit_view().as_view()(
            request,
            pk=kwargs[self.pk_url_name]
        )

    def render_delete_view(self, request, kwargs):
        return self.get_delete_view().as_view()(request)

    def get_add_view(self):
        NotImplementedError()

    def get_edit_view(self):
        NotImplementedError()

    def get_delete_view(self):
        NotImplementedError()


class ManageDashboardMixin(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True
    model = None
    main_list_url_name = None
    fields = []

    def get_success_url(self):
        return reverse_lazy(self.main_list_url_name)


class DashboardEditMixin(UpdateView):
    pk_url_name = "pk"

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get(self.pk_url_name))


class DashboardDeleteMixin:
    model = None
    main_list_url_name = ""

    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist("ids[]")
        for obj_id in obj_ids:
            obj = get_object_or_404(self.model, id=obj_id)
            obj.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(self.main_list_url_name)
