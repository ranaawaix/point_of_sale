# Generated by Django 3.2.22 on 2023-10-30 16:56

from django.db import migrations


def create_initial_data(apps, schema_editor):
    Store = apps.get_model('POS', 'Store')

    data = [{"name": "Ermanno Philip", "code": "d6f6c1f5-f343-40f3-9dfe-f8f1008ad74b",
             "email": "ephilip0@constantcontact.com", "address": "84 Superior Hill"},
            {"name": "Star Messent", "code": "82567841-08d9-4b76-ae67-06cb81d52143", "email": "smessent1@latimes.com",
             "address": "9517 Algoma Lane"},
            {"name": "Gennifer Hanse", "code": "01ac96a1-e9a9-4a07-808c-a3db509ef4ae", "email": "ghanse2@imageshack.us",
             "address": "4 Atwood Crossing"},
            {"name": "Ellyn Corish", "code": "88f68c40-c923-42ba-a5db-982e277988e6", "email": "ecorish3@hibu.com",
             "address": "5 Iowa Drive"}, {"name": "Terencio Shakesby", "code": "03e1d23f-276d-4889-afb6-19c0c8a74672",
                                          "email": "tshakesby4@prnewswire.com", "address": "35923 Eliot Place"}]

    for item in data:
        name = item['name']
        code = item['code']
        email = item['email']
        address = item['address']

        Store.objects.create(name=name, code=code, email=email, address=address)


class Migration(migrations.Migration):
    dependencies = [('POS', '0003_auto_20231030_0949'), ]

    operations = [
        migrations.RunPython(create_initial_data)
    ]
