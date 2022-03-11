from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonManageView.as_view(), name='person_list'),
    path('edit/<int:pk>/', views.PersonManageView.as_view(), name='person_edit')
]
