# Generated by Django 3.2.22 on 2023-10-31 06:44

from django.db import migrations


def create_initial_data(apps, schema_editor):
    Sale = apps.get_model('POS', 'Sale')
    Hold = apps.get_model('POS', 'Hold')

    data = [{"reference_note": "proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in"},
            {"reference_note": "metus vitae ipsum aliquam non"},
            {"reference_note": "ante vivamus tortor duis mattis egestas metus"},
            {"reference_note": "diam in magna bibendum imperdiet nullam orci pede"}, {
                "reference_note": "est phasellus sit amet erat nulla tempus vivamus in felis eu sapien cursus vestibulum proin"},
            {"reference_note": "morbi sem mauris laoreet ut rhoncus"},
            {"reference_note": "pede posuere nonummy integer non velit"},
            {"reference_note": "imperdiet sapien urna pretium nisl ut volutpat sapien"},
            {"reference_note": "tortor id nulla ultrices aliquet maecenas leo odio"},
            {"reference_note": "eget congue eget semper rutrum nulla nunc purus phasellus in"}, {
                "reference_note": "pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis"},
            {"reference_note": "semper porta volutpat quam pede lobortis ligula sit amet eleifend pede libero"},
            {"reference_note": "aliquam sit amet diam in magna"},
            {"reference_note": "sodales scelerisque mauris sit amet eros suspendisse accumsan tortor"},
            {"reference_note": "nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices"},
            {
                "reference_note": "cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel"},
            {"reference_note": "in libero ut massa volutpat convallis morbi odio odio elementum"},
            {"reference_note": "consequat dui nec nisi volutpat eleifend"},
            {"reference_note": "hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc"},
            {"reference_note": "suscipit ligula in lacus curabitur at ipsum"},
            {"reference_note": "rutrum ac lobortis vel dapibus at diam"},
            {"reference_note": "gravida sem praesent id massa"},
            {"reference_note": "odio justo sollicitudin ut suscipit a feugiat et eros vestibulum ac est lacinia"}, {
                "reference_note": "condimentum neque sapien placerat ante nulla justo aliquam quis turpis eget elit sodales"},
            {"reference_note": "pretium iaculis justo in hac habitasse platea dictumst etiam"},
            {"reference_note": "proin risus praesent lectus vestibulum quam sapien varius ut blandit"},
            {"reference_note": "augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur"}, {
                "reference_note": "porttitor lacus at turpis donec posuere metus vitae ipsum aliquam non mauris morbi non lectus"},
            {"reference_note": "rhoncus aliquet pulvinar sed nisl"},
            {"reference_note": "quis orci eget orci vehicula condimentum curabitur in libero ut"},
            {"reference_note": "hac habitasse platea dictumst morbi vestibulum"},
            {"reference_note": "in lectus pellentesque at nulla suspendisse potenti cras in purus eu magna"},
            {"reference_note": "mi integer ac neque duis bibendum morbi non quam nec dui luctus"},
            {"reference_note": "nullam orci pede venenatis non sodales sed tincidunt"},
            {"reference_note": "fermentum donec ut mauris eget massa"},
            {"reference_note": "convallis eget eleifend luctus ultricies eu nibh"},
            {"reference_note": "tempus semper est quam pharetra magna ac consequat metus"},
            {"reference_note": "quam pharetra magna ac consequat metus sapien ut nunc vestibulum"}, {
                "reference_note": "varius integer ac leo pellentesque ultrices mattis odio donec vitae nisi nam ultrices libero"},
            {"reference_note": "dictumst etiam faucibus cursus urna"},
            {"reference_note": "nulla ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo"},
            {"reference_note": "metus aenean fermentum donec ut mauris eget massa tempor convallis nulla"}, {
                "reference_note": "tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida nisi at nibh in"},
            {
                "reference_note": "condimentum neque sapien placerat ante nulla justo aliquam quis turpis eget elit sodales"},
            {"reference_note": "a libero nam dui proin leo odio porttitor"},
            {"reference_note": "platea dictumst maecenas ut massa quis augue luctus tincidunt nulla"},
            {"reference_note": "sem praesent id massa id nisl venenatis lacinia aenean"}, {
                "reference_note": "curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet"},
            {"reference_note": "sit amet nunc viverra dapibus nulla suscipit ligula in lacus"},
            {"reference_note": "eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero"}]

    sale = Sale.objects.get(id=2)

    for item in data:
        reference_note = item['reference_note']

        Hold.objects.create(reference_note=reference_note, sale=sale)


class Migration(migrations.Migration):
    dependencies = [('POS', '0010_auto_20231030_2337'), ]

    operations = [
        migrations.RunPython(create_initial_data)
    ]
