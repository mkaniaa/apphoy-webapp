from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField


class AccommodationCompany(models.Model):
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Name",
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
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address",
    )
    tin = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Tax Identification Number",
    )
    website = models.URLField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Website",
    )


class AccommodationCompanyStaff(models.Model):
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Name",
    )
    surname = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Name",
    )
    company = models.ForeignKey(
        AccommodationCompany,
        related_name="staff",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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


class Accommodation(models.Model):
    common_name = models.CharField(
        max_length=50,
        verbose_name="Name",
    )
    capacity = models.IntegerField(
        verbose_name="Capacity",
    )
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Address",
    )

    class Meta:
        abstract = True


class House(Accommodation):
    company = models.ForeignKey(
        AccommodationCompany,
        related_name="houses",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    square_footage = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Square footage",
    )
    floor_number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Number of floors",
    )
    room_number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Number of rooms",
    )


class Flat(Accommodation):
    company = models.ForeignKey(
        AccommodationCompany,
        related_name="flats",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    square_footage = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Square footage",
    )
    number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Flat number",
    )
    floor = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Floor",
    )


class Room(Accommodation):
    company = models.ForeignKey(
        AccommodationCompany,
        related_name="rooms",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    square_footage = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Square footage",
    )
    number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Room number",
    )
    floor = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Floor",
    )


class Tent(Accommodation):
    company = models.ForeignKey(
        AccommodationCompany,
        related_name="tents",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    room_number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Number of rooms",
    )


class Boat(Accommodation):
    BOAT_PROPULSION_CHOICES = [
        ("engine", "Engine"),
        ("sails", "Sails"),
        ("paddles", "Paddles"),
    ]

    company = models.ForeignKey(
        AccommodationCompany,
        related_name="boats",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    room_number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Number of rooms",
    )
    model = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Model",
    )
    built_year = models.DateField(
        null=True,
        blank=True,
        verbose_name="Year built",
    )
    main_propulsion = models.CharField(
        max_length=50,
        choices=BOAT_PROPULSION_CHOICES,
        null=True,
        blank=True,
        verbose_name="Main propulsion",
    )
    length = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Length",
    )
    height_inside = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Height inside",
    )
    sail_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Sail size",
    )
    engine_power = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Engine power",
    )
