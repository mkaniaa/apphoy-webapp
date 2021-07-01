from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripCreateView.as_view(), name='trip_list'),
    path('<int:trip_id>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
]
