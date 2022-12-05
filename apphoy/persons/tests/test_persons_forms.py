from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

from persons.forms import PersonManageForm
from persons.models import Person


class TestPersonManageForm(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPersonManageForm, cls).setUpClass()
        cls.credentials = {
            "username": "testuser",
            "password": "secret",
        }
        cls.user = User.objects.create_user(**cls.credentials)

    def test_empty_form(self):
        form = str(PersonManageForm())

        # Name
        self.assertInHTML(
            '<input type="text" name="name" maxlength="50" required id="id_name">', form,
        )
        # Surname
        self.assertInHTML(
            '<input type="text" name="surname" maxlength="50" required id="id_surname">', form,
        )
        # Phone number
        self.assertInHTML(
            '<input type="tel" name="phone_number" maxlength="128" id="id_phone_number">', form,
        )
        # E-mail
        self.assertInHTML(
            '<input type="email" name="email" maxlength="254" id="id_email">', form,
        )
        # Birthdate
        self.assertInHTML(
            '<input type="text" name="birth_date" class="date-picker" id="id_birth_date">', form,
        )
        # National Insurance Number
        self.assertInHTML(
            '<input type="text" name="nin" maxlength="50" id="id_nin">', form,
        )
        # Address
        self.assertInHTML(
            '<input type="text" name="address" maxlength="100" id="id_address">', form,
        )
        # T-Shirt size
        self.assertInHTML(
            '''
            <select name="t_shirt_size" id="id_t_shirt_size">
                <option value="" selected>---------</option>
                <option value="XS">XS</option>
                <option value="S">S</option>
                <option value="M">M</option>
                <option value="L">L</option>
                <option value="XL">XL</option>
                <option value="XXL">XXL</option>
                <option value="XXXL">XXXL</option>
            </select>
            ''',
            form,
        )
        # T-Shirt cut
        self.assertInHTML(
            '''
            <select name="t_shirt_cut" id="id_t_shirt_cut">
                <option value="" selected>---------</option>
                <option value="W">Woman</option>
                <option value="M">Man</option>
            </select>
            ''',
            form,
        )

    def test_add_person(self):
        request = HttpRequest()
        new_person_data = {
            "name": "Mark",
            "surname": "Kind",
            "phone_number": "+12125552368",
            "email": "test@email.com",
            "birth_date": "1994-06-03",
            "t_shirt_size": "L",
            "t_shirt_cut": "M",
        }
        request.POST = new_person_data

        self.assertEqual(Person.objects.count(), 0)
        form = PersonManageForm(request.POST)
        assert form.is_valid()
        form.save()

        self.assertEqual(Person.objects.count(), 1)
        person = Person.objects.first()
        assert person.name == new_person_data["name"]
        assert person.surname == new_person_data["surname"]
        assert person.phone_number == new_person_data["phone_number"]
        assert person.email == new_person_data["email"]
        assert datetime.strftime(person.birth_date, "%Y-%m-%d") == new_person_data["birth_date"]
        assert person.t_shirt_size == new_person_data["t_shirt_size"]
        assert person.t_shirt_cut == new_person_data["t_shirt_cut"]
