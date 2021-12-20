from django import forms
from django.utils.text import slugify

from common.models import get_field_names
from .models import Trip


class TripManageForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput, required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': "date-picker"}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': "date-picker"}))

    class Meta:
        model = Trip
        fields = get_field_names(model, exclude=["id", "stages"])

    def clean(self):
        cleaned_data = super(TripManageForm, self).clean()
        cleaned_data['slug'] = slugify(cleaned_data['name'])
        return cleaned_data
