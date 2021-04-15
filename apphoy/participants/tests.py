from django.test import TestCase

from participants.models import Participant


class ParticipantModelTests(TestCase):

    def test_get_field_names_all(self):
        """
        get_field_names() returns all model field names when argument exclude is not provided.
        :return:
        """
        field_names = [field.name for field in Participant._meta.get_fields()]
        self.assertCountEqual(Participant.get_field_names(), field_names)

    def test_get_field_names_without_id(self):
        """
        get_field_names() returns all model field names except 'id' when it is passed as an exclude parameter.
        :return:
        """
        field_names = [
            field.name
            for field in Participant._meta.get_fields()
            if field.name != 'id'
        ]
        self.assertCountEqual(Participant.get_field_names(exclude=['id']), field_names)
