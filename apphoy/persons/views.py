from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView

from common.models import get_field_names
from dashboard.mixins import DashboardListMixin
from dashboard.views import DashboardAddView, DashboardDeleteView, DashboardEditView
from .forms import PersonManageForm
from .models import Person


class PersonAddView(DashboardAddView):
    model = Person
    success_url = reverse_lazy("person_list")
    permission_required = "persons.add_person"
    form_class = PersonManageForm


class PersonEditView(DashboardEditView):
    model = Person
    permission_required = "persons.change_person"
    fields = get_field_names(model, exclude=['id'])


class PersonDeleteView(DashboardDeleteView):
    permission_required = "persons.delete_person"


class PersonManageView(DashboardListMixin, LoginRequiredMixin, ListView):
    model = Person
    template_name = "persons/dashboard_persons.html"
    dashboard_title = "Persons"
    edit_url_name = "person_edit"
    add_view = PersonAddView
    edit_view = DashboardEditView
    delete_view = PersonDeleteView
    pk = None

    def get_context_data(self, **kwargs):
        context = super(PersonManageView, self).get_context_data(**kwargs)
        context["target"] = self.pk

        if self.pk:
            person = get_object_or_404(self.model, pk=self.pk)
            context["form"] = PersonManageForm(instance=person)
        else:
            context["form"] = PersonManageForm

        return context
