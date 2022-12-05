from django import forms

from common.models import get_field_names
from .models import Person


class PersonManageForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "date-picker"}),
        required=False,
    )

    class Meta:
        model = Person
        fields = get_field_names(model, exclude="id")
