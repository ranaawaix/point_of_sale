# Generated by Django 3.2.22 on 2023-10-30 11:46

from django.db import migrations


def create_initial_data_1(apps, schema_editor):
    Barcode = apps.get_model('inventory', 'Barcode')
    data1 = [{'id': 51, "name": "EAN"}, {'id': 52, "name": "UPC"}, {'id': 53, "name": "ITF"}, {'id': 54, "name": "C39"},
             {'id': 55, "name": "CBR"}, {'id': 56, "name": "C28"}]

    for item in data1:
        id_value = item['id']
        name = item['name']

        Barcode.objects.create(id=id_value, name=name)


class Migration(migrations.Migration):
    dependencies = [('inventory', '0006_auto_20231030_0429'), ]

    operations = [migrations.RunPython(create_initial_data_1)]
