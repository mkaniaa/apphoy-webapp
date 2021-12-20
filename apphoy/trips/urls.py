from django.urls import path
from . import views


urlpatterns = [
    path('', views.TripManageView.as_view(), name='trip_list'),
    path('trip-no-permission/', views.TripManageNoPermissionView.as_view(), name='trip_no_permission'),
    path('edit/<int:pk>/', views.TripManageView.as_view(), name='trip_edit')
]