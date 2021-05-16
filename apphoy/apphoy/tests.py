from django.test import TestCase
from persons.models import Person
from .models import get_verbose_field_names, get_field_names


class PersonModelTests(TestCase):

    def test_get_field_names_all(self):
        """
        get_field_names() returns all model field names
        when argument exclude is not provided.
        """
        field_names = [field.name for field in Person._meta.get_fields()]
        self.assertCountEqual(get_field_names(Person), field_names)

    def test_get_field_names_without_id(self):
        """
        get_field_names() returns all model field names except 'id'
        when it is passed as an exclude parameter.
        """
        field_names = [
            field.name
            for field in Person._meta.get_fields()
            if field.name != 'id'
        ]
        self.assertCountEqual(get_field_names(Person, exclude=['id']), field_names)

    def test_get_verbose_field_names_without_id(self):
        """
        get_verbose_field_names() returns all model verbose field names except 'ID'
        when it is passed as an exclude parameter.
        """
        field_names = [
            field.verbose_name
            for field in Person._meta.get_fields()
            if field.verbose_name != 'ID'
        ]
        self.assertCountEqual(get_verbose_field_names(Person, exclude=['ID']), field_names)
