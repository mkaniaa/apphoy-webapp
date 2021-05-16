from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripStageListView.as_view(), name='trip_stages_list'),
]
