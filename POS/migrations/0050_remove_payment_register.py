# Generated by Django 3.2.23 on 2023-12-08 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0049_auto_20231207_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='register',
        ),
    ]