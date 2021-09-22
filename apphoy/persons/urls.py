from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.PersonManageView.as_view(), name='person_list'),
    path('no-permission/', views.PersonManageNoPermissionView.as_view(), name='no_permission'),
    path('edit/<int:pk>/', views.PersonManageView.as_view(), name='person_edit')
]
