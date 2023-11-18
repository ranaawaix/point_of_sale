# Generated by Django 3.2.22 on 2023-10-27 22:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=250),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.CharField(choices=[('A', 'Admin'), ('S', 'Staff')], default='S', max_length=250),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99999999999)]),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active')], default='Active', max_length=250),
        ),
    ]