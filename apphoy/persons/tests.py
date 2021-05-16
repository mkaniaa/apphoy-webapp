import mock
from django.test import TestCase

from persons.models import Person
from .templatetags import person_tags


class PersonTagsTests(TestCase):

    def test_attribute_value_person_name(self):
        """
        attribute_value() returns attribute value of the object if exists any with the name given as a string.
        """
        person = mock.Mock(spec=Person)
        person._state = mock.Mock()
        person.name = "Test"
        self.assertEqual(person_tags.attribute_value(person, 'name'), 'Test')

    def test_attribute_value_not_existing_attribute(self):
        """
        If there is no attribute with a name given as a string, attribute_value() returns None.
        """
        person = mock.Mock(spec=Person)
        person._state = mock.Mock()
        self.assertEqual(person_tags.attribute_value(person, 'test'), None)
