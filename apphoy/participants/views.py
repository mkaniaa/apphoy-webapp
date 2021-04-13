from django.views.generic.base import TemplateResponseMixin, View
from .models import Participant


class ParticipantListView(TemplateResponseMixin, View):
    model = Participant
    template_name = 'participants/participant/list.html'

    def get(self, request):
        participants = Participant.objects.all()
        return self.render_to_response({'participants': participants})
