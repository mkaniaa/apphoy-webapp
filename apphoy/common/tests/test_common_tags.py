import pytest
from mixer.backend.django import mixer

from common.templatetags import common_tags


@pytest.fixture
def person(request, db):
    return mixer.blend('persons.Person', attr=request.param)


@pytest.mark.parametrize('person', ['Test'], indirect=True)
def test_attribute_value_person_name(person):
    """
    attribute_value() returns attribute value of the object if exists any with the name given as a string.
    """
    assert common_tags.attribute_value(person, 'attr') == 'Test'


@pytest.mark.parametrize('person', ['Test'], indirect=True)
def test_attribute_value_not_existing_attribute(person):
    """
    If there is no attribute with a name given as a string, attribute_value() returns None.
    """
    assert common_tags.attribute_value(person, 'fake_attr') is None
