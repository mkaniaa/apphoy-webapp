import unittest

from apphoy.models import get_field_names, get_verbose_field_names
from persons.models import Person


def test_get_field_names_all():
    """
    get_field_names() called without "exclude" parameter
    returns names of all model fields
    """
    case = unittest.TestCase()
    original_field_names = [f.name for f in Person._meta.get_fields()]
    test_field_names = get_field_names(Person)
    case.assertCountEqual(original_field_names, test_field_names)


def test_get_field_names_exclude_id():
    """
    get_field_names() called with ['id'] passed in the "exclude" parameter
    returns names of all model fields except 'id' field
    """
    case = unittest.TestCase()
    original_field_names = [f.name for f in Person._meta.get_fields()]
    original_field_names.remove('id')
    test_field_names = get_field_names(Person, exclude=['id'])
    case.assertCountEqual(original_field_names, test_field_names)


def test_get_verbose_field_names_all():
    """
    get_verbose_field_names() called without "exclude" parameter
    returns verbose names of all model fields
    """
    case = unittest.TestCase()
    original_field_names = [f.verbose_name for f in Person._meta.get_fields()]
    test_field_names = get_verbose_field_names(Person)
    case.assertCountEqual(original_field_names, test_field_names)


def test_get_verbose_field_names_exclude_id():
    """
    get_verbose_field_names() called with ['ID'] passed in the "exclude" parameter
    returns names of all model fields except 'ID' field
    """
    case = unittest.TestCase()
    original_field_names = [f.verbose_name for f in Person._meta.get_fields()]
    original_field_names.remove('ID')
    test_field_names = get_verbose_field_names(Person, exclude=['ID'])
    case.assertCountEqual(original_field_names, test_field_names)
