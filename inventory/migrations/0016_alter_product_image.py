# Generated by Django 3.2.23 on 2023-11-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20231101_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
