# Generated by Django 3.2.23 on 2023-11-10 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0006_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
