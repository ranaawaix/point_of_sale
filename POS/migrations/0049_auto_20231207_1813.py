# Generated by Django 3.2.23 on 2023-12-07 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0048_storesale'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='register',
            field=models.ForeignKey(default=115, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='POS.register'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='StoreSale',
        ),
    ]
