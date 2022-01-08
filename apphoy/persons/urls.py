from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonManageView.as_view(), name='person_list'),
    path('person-no-permission/', views.PersonManageNoPermissionView.as_view(), name='person_no_permission'),
    path('edit/<int:pk>/', views.PersonManageView.as_view(), name='person_edit')
]
