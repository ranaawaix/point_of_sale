# Generated by Django 3.2.23 on 2023-11-07 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0026_alter_sale_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_payable',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]