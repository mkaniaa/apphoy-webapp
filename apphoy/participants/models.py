from django.db import models
from django.template.defaulttags import register


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

    name = models.CharField(max_length=50,
                            verbose_name='Name')
    surname = models.CharField(max_length=50,
                               verbose_name='Surname')
    phone = models.CharField(max_length=15,
                             null=True,
                             blank=True,
                             verbose_name='Phone number')
    email = models.EmailField(null=True,
                              blank=True,
                              verbose_name='E-mail')
    birth_date = models.DateTimeField(null=True,
                                      blank=True,
                                      verbose_name='Date of birth')
    nin = models.CharField(max_length=15,
                           null=True,
                           blank=True,
                           verbose_name='National Insurance number')
    city = models.CharField(max_length=20,
                            null=True,
                            blank=True,
                            verbose_name='City')
    t_shirt_size = models.CharField(max_length=4,
                                    choices=T_SHIRT_SIZE_CHOICES,
                                    null=True, blank=True,
                                    verbose_name='T-shirt size')
    t_shirt_cut = models.CharField(max_length=1,
                                   choices=T_SHIRT_CUT_CHOICES,
                                   null=True,
                                   blank=True,
                                   verbose_name='T-shirt cut')
    in_fb_group = models.BooleanField(null=True,
                                      blank=True,
                                      verbose_name='In Facebook group')
    fb_nickname = models.CharField(max_length=50,
                                   null=True,
                                   blank=True,
                                   verbose_name='Nickname on Facebook')

    @staticmethod
    def get_field_names(exclude=None):
        exclude = exclude if exclude else []
        return [
            field.name
            for field in Participant._meta.get_fields()
            if field.name not in exclude
        ]

    @staticmethod
    @register.simple_tag
    def get_verbose_field_names(exclude=None):
        exclude = exclude if exclude else []
        return [
            field.verbose_name
            for field in Participant._meta.get_fields()
            if field.verbose_name not in exclude
        ]