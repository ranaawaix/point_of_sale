# Generated by Django 3.2.23 on 2023-11-20 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
