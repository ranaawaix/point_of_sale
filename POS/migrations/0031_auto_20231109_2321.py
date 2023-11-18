# Generated by Django 3.2.23 on 2023-11-09 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0030_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='order_tax',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_payable',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
