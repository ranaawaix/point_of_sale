# Generated by Django 3.2.22 on 2023-10-30 17:16

from django.db import migrations


def create_initial_data(apps, schema_editor):
    StoreProduct = apps.get_model('POS', 'StoreProduct')
    Store = apps.get_model('POS', 'Store')
    Product = apps.get_model('inventory', 'Product')

    data = [{"quantity": 51}, {"quantity": 931}, {"quantity": 320}, {"quantity": 451}, {"quantity": 995}]

    for item in data:
        quantity = item['quantity']

        StoreProduct.objects.create(store=Store.objects.get(id=1), product=Product.objects.get(id= 1), quantity=quantity)


class Migration(migrations.Migration):
    dependencies = [('POS', '0005_alter_storeproduct_price'), ]

    operations = [
        migrations.RunPython(create_initial_data)
    ]
