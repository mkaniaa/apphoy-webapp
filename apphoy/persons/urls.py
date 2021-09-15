from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonManageView.as_view(), name='person_list'),
    path('no_permission/', views.PersonManageView.as_view(), name='no_permission'),
    path('edit/<int:pk>/', views.PersonManageView.as_view(), name='person_edit')
]
