# Generated by Django 3.2.23 on 2023-11-06 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0019_alter_sale_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_payable',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
