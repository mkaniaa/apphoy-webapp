from django.db import models


class Participant(models.Model):
    WOMAN = 'W'
    MAN = 'M'
    T_SHIRT_CUT_CHOICES = [
        (WOMAN, 'Woman'),
        (MAN, 'Man'),
    ]
    T_SHIRT_SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    ]

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    nin = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    t_shirt_size = models.CharField(max_length=4, choices=T_SHIRT_SIZE_CHOICES, null=True, blank=True)
    t_shirt_cut = models.CharField(max_length=1, choices=T_SHIRT_CUT_CHOICES, null=True, blank=True)
    in_fb_group = models.BooleanField(null=True, blank=True)
    fb_nickname = models.CharField(max_length=50, null=True, blank=True)

