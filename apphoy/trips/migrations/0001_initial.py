# Generated by Django 3.2.16 on 2022-11-09 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('start_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Start address')),
                ('final_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Final address')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TripStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
                ('start_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Start address')),
                ('final_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Final address')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='trips.trip')),
            ],
        ),
    ]
