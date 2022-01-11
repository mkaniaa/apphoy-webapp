from django.urls import reverse

from trips.forms.trip_stage import TripStageManageForm


def test_person_manage_view_add_form(self):
    response = self.client.get(reverse('person_list'))
    mock_form = TripStageManageForm
    response_form = response.context['form']

    self.assertEqual(response_form().data, mock_form().data)
