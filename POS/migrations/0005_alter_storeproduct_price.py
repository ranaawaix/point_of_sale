# Generated by Django 3.2.22 on 2023-10-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0004_auto_20231030_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeproduct',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]