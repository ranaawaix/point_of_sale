# Generated by Django 3.2.23 on 2023-11-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0021_alter_sale_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='discount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('H', 'Held'), ('P', 'Paid')], default='H', max_length=250),
        ),
    ]
