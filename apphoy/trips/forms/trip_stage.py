from django import forms
from django.utils.text import slugify

from common.models import get_field_names
from trips.models import TripStage


class TripStageManageForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.HiddenInput, required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': "date-picker"}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': "date-picker"}))

    class Meta:
        model = TripStage
        fields = get_field_names(model, exclude=["id", "trip"])

    def clean(self):
        cleaned_data = super(TripStageManageForm, self).clean()
        cleaned_data['slug'] = slugify(cleaned_data['name'])
        # cleaned_data['trip'] = self.instance.
        return cleaned_data
