# Generated by Django 3.2.11 on 2022-01-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('surname', models.CharField(max_length=50, verbose_name='Surname')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('nin', models.CharField(blank=True, max_length=15, null=True, verbose_name='National Insurance Number')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='City')),
                ('t_shirt_size', models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=4, null=True, verbose_name='T-shirt size')),
                ('t_shirt_cut', models.CharField(blank=True, choices=[('W', 'Woman'), ('M', 'Man')], max_length=1, null=True, verbose_name='T-shirt cut')),
                ('in_fb_group', models.BooleanField(blank=True, null=True, verbose_name='In Facebook group')),
                ('fb_nickname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nickname on Facebook')),
            ],
        ),
    ]
