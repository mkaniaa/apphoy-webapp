from django.urls import path

from .views import trip, trip_stage

urlpatterns = [
    path("", trip.TripManageView.as_view(), name="trip_list"),
    path("<int:trip_pk>/stages/", trip_stage.TripStageManageView.as_view(), name="trip_stage_list"),
    path(
        "<int:trip_pk>/stages/<int:trip_stage_pk>/edit/",
        trip_stage.TripStageManageView.as_view(),
        name="trip_stage_edit"
    ),
    path("<int:trip_pk>/edit/", trip.TripEditView.as_view(), name="trip_edit")
]
