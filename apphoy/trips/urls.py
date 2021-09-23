from django.urls import path
from . import views

urlpatterns = [
    path('', views.TripManageView.as_view(), name='trip_list'),
    path('<int:trip_id>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
    path('edit/<int:pk>/', views.TripEditView.as_view(), name='trip_edit')
]
