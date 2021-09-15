import pytest
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

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
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)

    def setUp(self):
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])

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

    def test_person_add_view_authorised(self):
        request = self.factory.post(reverse('person_list'), {'action': 'Add',
                                                             'name': self.person.name,
                                                             'surname': self.person.surname})
        permission = Permission.objects.get(codename='add_person')
        self.user.user_permissions.add(permission)
        self.user = get_object_or_404(User, pk=self.user.id)
        request.user = self.user
        response = PersonManageView.as_view()(request)
        self.assertRedirects(response, '/persons/', fetch_redirect_response=False)
        self.assertEqual(Person.objects.last().name, self.person.name)

    def test_person_add_view_unauthorised(self):
        response = self.client.post(reverse('person_list'), {'action': 'Add',
                                                             'name': self.person.name,
                                                             'surname': self.person.surname}, follow=True)
        messages = [str(m) for m in response.context['messages']]
        self.assertRedirects(response, '/persons/no_permission/', fetch_redirect_response=False)
        self.assertEqual('You have no permission for this action!', messages[0])
