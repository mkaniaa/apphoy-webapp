from django import forms
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from common.models import get_field_names
from trips.models import TripStage, Trip


class TripStageManageForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput, required=False)
    trip = forms.CharField(widget=forms.HiddenInput, required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': "date-picker"}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': "date-picker"}))

    class Meta:
        model = TripStage
        fields = get_field_names(model, exclude=["id"])

    def __init__(self, *args, **kwargs):
        if kwargs.get("initial"):
            self.trip_pk = kwargs["initial"].pop("trip_pk")
        print(kwargs)
        super(TripStageManageForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TripStageManageForm, self).clean()
        cleaned_data['slug'] = slugify(cleaned_data['name'])
        cleaned_data['trip'] = get_object_or_404(Trip, pk=self.trip_pk)
        return cleaned_data
