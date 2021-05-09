from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.ParticipantAddView.as_view(), name='participant_add'),
    path('<pk>/edit/', views.ParticipantEditView.as_view(), name='participant_edit'),
    path('<int:participant_id>/delete/', views.ParticipantDeleteView.as_view(), name='participant_delete'),
]
