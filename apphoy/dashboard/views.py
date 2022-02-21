from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View, TemplateResponseMixin


class ManageDashboardMixin(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True
    model = None
    main_list_url_name = None
    success_url = reverse_lazy(main_list_url_name)


class DashboardAddView(ManageDashboardMixin, CreateView):
    ...


class DashboardEditView(ManageDashboardMixin, UpdateView):

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get("pk"))


class DashboardDeleteView(ManageDashboardMixin, View):

    def post(self, request, *args, **kwargs):
        obj_ids = request.POST.getlist('ids[]')
        for obj_id in obj_ids:
            obj = get_object_or_404(self.model, id=obj_id)
            obj.delete()
        return redirect(reverse(self.main_list_url_name))


class DashboardNoPermissionView(TemplateResponseMixin, View):
    template_name = 'dashboard/dashboard_no_permission.html'
