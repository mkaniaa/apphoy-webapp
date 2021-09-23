from django import forms

from common.models import get_field_names
from .models import Person


class PersonManageForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = get_field_names(model, exclude='id')
