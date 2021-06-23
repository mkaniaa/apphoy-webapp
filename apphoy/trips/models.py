from django.db import models


class Trip(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class TripStage(models.Model):
    trip = models.ForeignKey(Trip, related_name='stages', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    start_date = models.DateField(null=True,
                                  blank=True,
                                  verbose_name='Start date')
    end_date = models.DateField(null=True,
                                blank=True,
                                verbose_name='End date')
    start_address = models.CharField(max_length=100,
                                     null=True,
                                     blank=True,
                                     verbose_name='Start address')
    final_address = models.CharField(max_length=100,
                                     null=True,
                                     blank=True,
                                     verbose_name='Final address')

