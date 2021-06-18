from django.contrib import admin

from apphoy.models import get_field_names
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = get_field_names(Person, exclude=['id'])
