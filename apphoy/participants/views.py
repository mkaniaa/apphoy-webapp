from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Participant


class ParticipantListView(ListView):
    model = Participant
    template_name = 'participants/manage/participant/list.html'


class ManageParticipantMixin(LoginRequiredMixin, PermissionRequiredMixin):
    model = Participant
    fields = Participant.get_field_names(exclude=['id'])
    success_url = reverse_lazy('participant_list')


class ParticipantAddView(ManageParticipantMixin,
                         CreateView):
    template_name = 'participants/manage/participant/form.html'
    permission_required = 'participant.add_participant'


class ParticipantEditView(ManageParticipantMixin,
                          UpdateView):
    template_name = 'participants/manage/participant/form.html'
    permission_required = 'participant.change_participant'


class ParticipantDeleteView(ManageParticipantMixin,
                            DeleteView):
    template_name = 'participants/manage/participant/delete.html'
    permission_required = 'participant.delete_participant'