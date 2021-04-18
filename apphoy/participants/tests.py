import mock
from django.test import TestCase

from participants.models import Participant
from .templatetags import participant_tags


class ParticipantModelTests(TestCase):

    def test_get_field_names_all(self):
        """
        get_field_names() returns all model field names
        when argument exclude is not provided.
        """
        field_names = [field.name for field in Participant._meta.get_fields()]
        self.assertCountEqual(Participant.get_field_names(), field_names)

    def test_get_field_names_without_id(self):
        """
        get_field_names() returns all model field names except 'id'
        when it is passed as an exclude parameter.
        """
        field_names = [
            field.name
            for field in Participant._meta.get_fields()
            if field.name != 'id'
        ]
        self.assertCountEqual(Participant.get_field_names(exclude=['id']), field_names)

    def test_get_verbose_field_names_without_id(self):
        """
        get_verbose_field_names() returns all model verbose field names except 'ID'
        when it is passed as an exclude parameter.
        """
        field_names = [
            field.verbose_name
            for field in Participant._meta.get_fields()
            if field.verbose_name != 'ID'
        ]
        self.assertCountEqual(Participant.get_verbose_field_names(exclude=['ID']), field_names)


class ParticipantTagsTests(TestCase):

    def test_attribute_value_participant_name(self):
        """
        attribute_value() returns attribute value of the object if exists any with the name given as a string.
        """
        participant = mock.Mock(spec=Participant)
        participant._state = mock.Mock()
        participant.name = "Test"
        self.assertEqual(participant_tags.attribute_value(participant, 'name'), 'Test')

    def test_attribute_value_not_existing_attribute(self):
        """
        If there is no attribute with a name given as a string, attribute_value() returns None.
        """
        participant = mock.Mock(spec=Participant)
        participant._state = mock.Mock()
        self.assertEqual(participant_tags.attribute_value(participant, 'test'), None)
