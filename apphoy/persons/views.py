from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import View

from apphoy.models import get_verbose_field_names, get_field_names
from .forms import PersonManageForm
from .models import Person


class PersonManageView(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'persons/dashboard_persons.html'
    pk = None

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, exclude='ID')
        attributes = get_field_names(self.model, exclude='id')
        context = super(PersonManageView, self).get_context_data(**kwargs)
        context['headers'] = headers
        context['attributes'] = attributes
        context['target'] = self.pk

        if self.pk:
            person = get_object_or_404(self.model, pk=self.pk)
            context['form'] = PersonManageForm(instance=person)
        else:
            context['form'] = PersonManageForm

        return context

    def get(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        return super(PersonManageView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST['action'] == 'Add':
            return PersonAddView.as_view()(request)
        elif request.POST['action'] == 'Update':
            return PersonEditView.as_view()(request, pk=kwargs['pk'])
        else:
            return PersonDeleteView.as_view()(request)


class ManagePersonMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Person
    success_url = reverse_lazy('person_list')


class PersonDeleteView(View, ManagePersonMixin):
    permission_required = 'person.delete_person'

    def post(self, request, *args, **kwargs):
        person_ids = request.POST.getlist('ids[]')
        for person_id in person_ids:
            person = get_object_or_404(Person, id=person_id)
            person.delete()
        return redirect('person_list')


class PersonAddView(CreateView, ManagePersonMixin):
    model = Person
    success_url = '/persons/'
    permission_required = 'person.add_person'
    fields = get_field_names(model, exclude=['id'])


class PersonEditView(ManagePersonMixin, UpdateView):
    model = Person
    permission_required = 'person.change_person'
    fields = get_field_names(model, exclude=['id'])

    def get_object(self, queryset=None):
        return Person.objects.get(pk=self.kwargs.get("pk"))
