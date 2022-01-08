from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.base import View

from common.models import get_verbose_field_names, get_field_names
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
        try:
            if request.POST['action'] == 'Add':
                return PersonAddView.as_view()(request)
            elif request.POST['action'] == 'Update':
                return PersonEditView.as_view()(request, pk=kwargs['pk'])
            else:
                return PersonDeleteView.as_view()(request)
        except PermissionDenied:
            return redirect(reverse('person_no_permission'))


class PersonManageNoPermissionView(PersonManageView):
    template_name = 'persons/dashboard_persons_no_permission.html'


class ManagePersonMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Person
    success_url = reverse_lazy('person_list')
    raise_exception = True


class PersonDeleteView(ManagePersonMixin, View):
    permission_required = 'persons.delete_person'

    def post(self, request, *args, **kwargs):
        person_ids = request.POST.getlist('ids[]')
        for person_id in person_ids:
            person = get_object_or_404(Person, id=person_id)
            person.delete()
        return redirect(reverse('person_list'))


class PersonAddView(ManagePersonMixin, CreateView):
    model = Person
    success_url = reverse_lazy('person_list')
    permission_required = 'persons.add_person'
    form_class = PersonManageForm


class PersonEditView(ManagePersonMixin, UpdateView):
    model = Person
    permission_required = 'persons.change_person'
    fields = get_field_names(model, exclude=['id'])

    def get_object(self, queryset=None):
        return Person.objects.get(pk=self.kwargs.get("pk"))
