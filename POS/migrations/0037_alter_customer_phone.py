# Generated by Django 3.2.23 on 2023-11-20 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0036_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
    ]