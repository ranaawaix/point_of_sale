# Generated by Django 3.2.23 on 2023-11-20 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0035_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
