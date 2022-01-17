import datetime

import pytest
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from trips.models import TripStage, Trip
from trips.views.trip_stages import TripStagesManageView


@pytest.mark.django_db
class TestTripStagesViews(TestCase):

    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super(TestTripStagesViews, cls).setUpClass()
        cls.trip_data = {
            'name': 'Test Trip Name',
            'start_date': datetime.date(2021, 12, 31),
            'end_date': datetime.date(2022, 1, 14),
            'start_address': 'Test Address',
            'final_address': 'Test Address',
        }
        cls.trip = Trip.objects.create(**cls.trip_data)
        cls.trip_stage_data = {
            'name': 'Test Trip Stage Name',
            'order': 1,
            'start_date': datetime.date(2021, 12, 31),
            'end_date': datetime.date(2022, 1, 14),
            'start_address': 'Test Address',
            'final_address': 'Test Address',
        }
        cls.factory = RequestFactory()
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)

    def test_trip_stage_add_view_authorised(self):
        request = self.factory.post(
            reverse('trip_stages', kwargs={"trip_pk": self.trip.pk}),
            {'action': 'Add', **self.trip_stage_data}
        )
        permission = Permission.objects.get(codename='add_tripstage')
        self.user.user_permissions.add(permission)
        self.user = get_object_or_404(User, pk=self.user.id)
        request.user = self.user
        response = TripStagesManageView.as_view()(request)

        self.assertRedirects(
            response,
            reverse('trip_stages', kwargs={"trip_pk": self.trip.pk}),
            fetch_redirect_response=False
        )
        self.assertEqual(TripStage.objects.last().name, self.trip_stage_data["name"])
