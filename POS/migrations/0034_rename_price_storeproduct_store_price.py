# Generated by Django 3.2.23 on 2023-11-13 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0033_alter_storeproduct_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storeproduct',
            old_name='price',
            new_name='store_price',
        ),
    ]
