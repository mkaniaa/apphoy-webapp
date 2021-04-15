from django.contrib import admin
from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = Participant.get_field_names()
    search_fields = ('name', 'surname')
    ordering = ('name', 'surname')
