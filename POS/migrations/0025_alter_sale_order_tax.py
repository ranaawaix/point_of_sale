# Generated by Django 3.2.23 on 2023-11-07 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0024_auto_20231106_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='order_tax',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
