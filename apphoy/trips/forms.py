from django import forms
from django.utils.text import slugify

from .models import Trip


class TripCreateForm(forms.ModelForm):
    name = forms.TextInput()
    slug = forms.SlugField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Trip
        fields = ('name', 'slug',)

    def clean(self):
        cleaned_data = super(TripCreateForm, self).clean()
        cleaned_data['slug'] = slugify(cleaned_data['name'])
        return cleaned_data
