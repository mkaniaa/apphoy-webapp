from django.views.generic.base import View, TemplateResponseMixin


class DashboardNoPermissionView(TemplateResponseMixin, View):
    template_name = 'dashboard/dashboard_no_permission.html'
