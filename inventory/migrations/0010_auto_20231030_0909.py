# Generated by Django 3.2.22 on 2023-10-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20231030_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]