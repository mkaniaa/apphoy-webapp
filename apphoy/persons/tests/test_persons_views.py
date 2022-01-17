import pytest
from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from persons.forms import PersonManageForm
from persons.models import Person
from persons.views import PersonManageView


@pytest.mark.django_db
class TestPersonsViews(TestCase):

    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super(TestPersonsViews, cls).setUpClass()
        cls.person_data = {"name": 'TestName', "surname": 'TestSurname'}
        cls.person = Person.objects.create(**cls.person_data)
        cls.factory = RequestFactory()
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        cls.user = User.objects.create_user(**cls.credentials)

    def setUp(self):
        self.client.login(**self.credentials)
        self.all_persons = Person.objects.all()

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
        response = self.client.get(reverse('person_edit', kwargs={'pk': self.person.id}))

        self.assertEqual(response.context['target'], self.person.id)

    def test_person_manage_view_add_form(self):
        response = self.client.get(reverse('person_list'))
        mock_form = PersonManageForm
        response_form = response.context['form']

        self.assertEqual(response_form().data, mock_form().data)

    def test_person_manage_view_update_form(self):
        response = self.client.get(reverse('person_edit', kwargs={'pk': self.person.id}))
        mock_form = PersonManageForm(instance=self.person)
        response_form = response.context['form']

        self.assertEqual(response_form.data, mock_form.data)

    def test_person_add_view_unauthorised(self):
        response = self.client.post(reverse('person_list'), {'action': 'Add',
                                                             'name': self.person.name,
                                                             'surname': self.person.surname}, follow=True)
        self.assertRedirects(response, reverse('person_list') + 'person-no-permission/', fetch_redirect_response=False)

    def test_person_add_view_authorised(self):
        request = self.factory.post(reverse('person_list'), {'action': 'Add',
                                                             'name': self.person.name,
                                                             'surname': self.person.surname})
        permission = Permission.objects.get(codename='add_person')
        self.user.user_permissions.add(permission)
        self.user = get_object_or_404(User, pk=self.user.id)
        request.user = self.user
        response = PersonManageView.as_view()(request)

        self.assertRedirects(response, reverse('person_list'), fetch_redirect_response=False)
        self.assertEqual(Person.objects.last().name, self.person.name)

    def test_person_edit_view_unauthorised(self):
        person = Person.objects.get(**self.person_data)
        data = self.person_data.copy()
        data['action'] = 'Update'
        data['email'] = 'test@test.com'
        response = self.client.post(reverse('person_edit', kwargs={'pk': person.id}), data, follow=True)
        self.assertRedirects(response, reverse('person_list') + 'person-no-permission/', fetch_redirect_response=False)

        person.refresh_from_db()
        self.assertEqual(person.email, None)

    def test_person_edit_view_authorised(self):
        person = Person.objects.get(**self.person_data)
        data = self.person_data.copy()
        data['action'] = 'Update'
        data['email'] = 'test@test.com'
        request = self.factory.post(reverse('person_edit', kwargs={'pk': person.id}), data)
        permission = Permission.objects.get(codename='change_person')
        self.user.user_permissions.add(permission)
        self.user = get_object_or_404(User, pk=self.user.id)
        request.user = self.user

        response = PersonManageView.as_view()(request, pk=person.id)
        self.assertRedirects(response, reverse('person_list'), fetch_redirect_response=False)

        person.refresh_from_db()
        self.assertEqual(person.email, 'test@test.com')

    def test_person_delete_view_unauthorised(self):
        person = Person.objects.get(**self.person_data)
        response = self.client.post(reverse('person_list'), {'action': 'Delete', 'ids[]': [person.id]}, follow=True)
        self.assertRedirects(response, reverse('person_list') + 'person-no-permission/', fetch_redirect_response=False)

        self.assertTrue(Person.objects.filter(pk=person.id).exists())

    def test_person_delete_view_authorised(self):
        person = Person.objects.get(**self.person_data)
        request = self.factory.post(reverse('person_list'), {'action': 'Delete', 'ids[]': [person.id]})
        permission = Permission.objects.get(codename='delete_person')
        self.user.user_permissions.add(permission)
        self.user = get_object_or_404(User, pk=self.user.id)
        request.user = self.user
        response = PersonManageView.as_view()(request)

        self.assertRedirects(response, reverse('person_list'), fetch_redirect_response=False)
        self.assertFalse(Person.objects.filter(pk=person.id).exists())
