from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    WOMAN = "W"
    MAN = "M"
    T_SHIRT_CUT_CHOICES = [
        (WOMAN, "Woman"),
        (MAN, "Man"),
    ]
    T_SHIRT_SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("XXXL", "XXXL"),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name="Name",
    )
    surname = models.CharField(
        max_length=50,
        verbose_name="Surname",
    )
    phone_numbers = ArrayField(
        PhoneNumberField(blank=True),
        null=True,
        verbose_name="Phone numbers",
    )
    emails = ArrayField(
        models.EmailField(blank=True),
        null=True,
        verbose_name="E-mail addresses",
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of birth",
    )
    nin = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="National Insurance Number",
    )
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address",
    )
    t_shirt_size = models.CharField(
        max_length=4,
        choices=T_SHIRT_SIZE_CHOICES,
        null=True,
        blank=True,
        verbose_name="T-shirt size",
    )
    t_shirt_cut = models.CharField(
        max_length=1,
        choices=T_SHIRT_CUT_CHOICES,
        null=True,
        blank=True,
        verbose_name="T-shirt cut",
    )
