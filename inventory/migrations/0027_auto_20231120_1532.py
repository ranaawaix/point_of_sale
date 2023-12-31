# Generated by Django 3.2.23 on 2023-11-20 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0026_alter_supplier_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='user_accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='user_accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='user_accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='purchaseorders', to='user_accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='user_accounts.user'),
            preserve_default=False,
        ),
    ]
