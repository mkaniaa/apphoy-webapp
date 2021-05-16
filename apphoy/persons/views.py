from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from apphoy.models import get_verbose_field_names, get_field_names
from .models import Person


class PersonListView(ListView):
    model = Person
    template_name = 'persons/list.html'

    def get_context_data(self, **kwargs):
        headers = get_verbose_field_names(self.model, 'ID')
        attributes = get_field_names(self.model, 'id')
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['headers'] = headers
        context['attributes'] = attributes
        return context

    def post(self, request):
        return PersonDeleteView.as_view()(request)


class PersonDeleteView(View):
    def post(self, request, *args, **kwargs):
        person_ids = request.POST.getlist('ids[]')
        for person_id in person_ids:
            person = get_object_or_404(Person, id=person_id)
            person.delete()
        return redirect('person_list')


class ManagePersonMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Person
    fields = get_field_names(model, exclude=['id'])
    success_url = reverse_lazy('person_list')


class PersonAddView(ManagePersonMixin, CreateView):
    template_name = 'persons/manage/person/form.html'
    permission_required = 'person.add_person'


class PersonEditView(ManagePersonMixin, UpdateView):
    template_name = 'persons/manage/person/form.html'
    permission_required = 'person.change_person'
