# Generated by Django 3.2.23 on 2023-11-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0040_auto_20231122_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pos',
            name='opening_cash_in_hand',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
