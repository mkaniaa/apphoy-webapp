from django.urls import path
from . import views

urlpatterns = [
    path('', views.PersonListView.as_view(), name='person_list'),
    path('add/', views.PersonAddView.as_view(), name='person_add'),
    path('<pk>/edit/', views.PersonEditView.as_view(), name='person_edit'),
    path('<int:person_id>/delete/', views.PersonDeleteView.as_view(), name='person_delete'),
]
