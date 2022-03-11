from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import View
from common.models import get_field_names
from dashboard.mixins import DashboardListMixin, ManageDashboardMixin, DashboardEditMixin, DashboardDeleteMixin
from .forms import PersonManageForm
from .models import Person


class ManagePersonMixin(ManageDashboardMixin):
    model = Person
    main_list_url_name = "person_list"
    fields = get_field_names(model, exclude=['id'])


class PersonAddView(ManagePersonMixin, CreateView):
    fields = None  # Specifying both 'fields' and 'form_class' is not permitted.
    permission_required = "persons.add_person"
    form_class = PersonManageForm


class PersonEditView(ManagePersonMixin, DashboardEditMixin, UpdateView):
    permission_required = "persons.change_person"


class PersonDeleteView(ManagePersonMixin, DashboardDeleteMixin, View):
    permission_required = "persons.delete_person"


class PersonManageView(DashboardListMixin, LoginRequiredMixin, ListView):
    model = Person
    dashboard_title = "Persons"
    main_url_name = "person_list"
    edit_url_name = "person_edit"
    form = PersonManageForm
    person_pk = None

    def get_context_data(self, **kwargs):
        context = super(PersonManageView, self).get_context_data(**kwargs)
        context["target"] = self.person_pk

        if self.person_pk:
            person = get_object_or_404(self.model, pk=self.person_pk)
            context["form"] = self.form(instance=person)
        else:
            context["form"] = self.form

        return context

    def get(self, request, *args, **kwargs):
        self.person_pk = kwargs.get(self.pk_url_name)
        return super(PersonManageView, self).get(request, *args, **kwargs)

    def get_add_view(self):
        return PersonAddView

    def get_edit_view(self):
        return PersonEditView

    def get_delete_view(self):
        return PersonDeleteView
