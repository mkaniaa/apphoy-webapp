from django.urls import path

from . import views

urlpatterns = [
    path("no-permission/", views.DashboardNoPermissionView.as_view(), name="no_permission"),
]
