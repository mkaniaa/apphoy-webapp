from django.contrib import admin

from common.models import get_field_names
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = get_field_names(Trip, exclude=['id', 'stages'])
