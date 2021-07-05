import unittest

import pytest
from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.test import TestCase, Client

from persons.forms import PersonManageForm
from persons.models import Person
from persons.views import PersonManageView

TEST_ID = 1
TEST_NAME = 'TestName'
TEST_SURNAME = 'TestSurname'


@pytest.mark.django_db
class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        cls.person = mixer.blend('persons.Person',
                                 id=TEST_ID,
                                 name=TEST_NAME,
                                 surname=TEST_SURNAME)
        cls.factory = RequestFactory()

    def test_person_manage_view_headers_context(self):
        response = self.client.get(reverse('person_list'))
        original_verbose_field_names = [f.verbose_name for f in Person._meta.get_fields()]
        original_verbose_field_names.remove('ID')
        self.assertCountEqual(response.context['headers'], original_verbose_field_names)

    def test_person_manage_view_attributes_context(self):
        response = self.client.get(reverse('person_list'))
        original_field_names = [f.name for f in Person._meta.get_fields()]
        original_field_names.remove('id')
        self.assertCountEqual(response.context['attributes'], original_field_names)

    def test_person_manage_view_target_context(self):
        response = self.client.get(reverse('person_edit', kwargs={'pk': TEST_ID}))
        self.assertEqual(response.context['target'], TEST_ID)

    def test_person_manage_view_add_form(self):
        response = self.client.get(reverse('person_list'))
        mock_form = PersonManageForm
        response_form = response.context['form']
        self.assertEqual(response_form().data, mock_form().data)

    def test_person_manage_view_update_form(self):
        response = self.client.get(reverse('person_edit', kwargs={'pk': TEST_ID}))
        mock_form = PersonManageForm(instance=self.person)
        response_form = response.context['form']
        self.assertEqual(response_form.data, mock_form.data)

    def test_person_add_view_authenticated(self):
        request = self.factory.post(reverse('person_list'), {'action': 'Add',
                                                             'name': TEST_NAME,
                                                             'surname': TEST_SURNAME})
        request.user = User()
        self.assertEqual(Person.objects.last().name, TEST_NAME)
        Person.objects.last().delete()

    def test_person_add_view_unauthenticated(self):
        request = self.factory.post(reverse('person_list'), {'action': 'Add',
                                                             'name': TEST_NAME,
                                                             'surname': TEST_SURNAME})
        request.user = AnonymousUser()
        self.assertEqual(Person.objects.last().name, TEST_NAME)
        Person.objects.last().delete()

    # def test_product_detail_unauthenticated(self):
    #     path = reverse('detail', kwargs={'pk': 1})
    #     request = self.factory.get(path)
    #     request.user = AnonymousUser()
    #
    #     response = product_detail(request, pk=1)
    #     assert 'accounts/login' in response.url



# def setUp(self):
#     self.request_factory = RequestFactory()
#     self.user = User.objects.create_user(
#         username='javed', email='javed@javed.com', password='my_secret')
#
# def test_my_test_method(self):
#     request = self.request_factory.post(reverse('home'), {'question_title_name':'my first question title', 'question_name':'my first question', 'question_tag_name':'first, question'})
#     request.user = self.user
#     response = home_page(request)