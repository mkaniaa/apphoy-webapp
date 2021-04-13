from django.contrib import admin
from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Participant._meta.get_fields()]
    search_fields = ('name', 'surname')
    ordering = ('name', 'surname')
