from django.urls import path

from .views import trip, trip_stages

urlpatterns = [
    path('', trip.TripManageView.as_view(), name='trip_list'),
    path('trip-no-permission/', trip.TripManageNoPermissionView.as_view(), name='trip_no_permission'),
    path('<int:trip_pk>/stages/', trip_stages.TripStagesManageView.as_view(), name='trip_stages'),
    path('<int:trip_pk>/stages/<int:trip_stage_pk>/edit/', trip_stages.TripStagesManageView.as_view(), name='trip_stage_edit'),
    path('edit/<int:pk>/', trip.TripManageView.as_view(), name='trip_edit')
]