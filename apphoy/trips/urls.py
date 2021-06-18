from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripListView.as_view(), name='trip_list'),
    path('add/', views.TripAddView.as_view(), name='trip_add'),
    path('<pk>/edit/', views.TripEditView.as_view(), name='trip_edit'),
    path('<int:trip_id>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
]
