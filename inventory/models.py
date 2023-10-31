import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.PositiveIntegerField(validators=[MaxValueValidator(99999999999)], null=True, blank=True)
    supplier_custom_field_1 = models.CharField(max_length=250, null=True, blank=True)
    supplier_custom_field_2 = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.id}-{self.name}'


class ProductType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


BARCODE_CHOICES = [
    ('EAN', 'EAN'),
    ('UPC', 'UPC'),
    ('ITF', 'ITF'),
    ('C39', 'CODE39'),
    ('CBR', 'CODABAR'),
    ('C28', 'CODE128'),
]


class Barcode(models.Model):
    name = models.CharField(choices=BARCODE_CHOICES, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.name


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
TAX_CHOICES = [
    ('In', 'Inclusive'),
    ('Ex', 'Exclusive'),
]


class Product(models.Model):
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    barcode_symbology = models.ForeignKey(Barcode, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    cost = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    product_tax = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                      validators=PERCENTAGE_VALIDATOR)
    tax_method = models.CharField(max_length=250, choices=TAX_CHOICES)
    alert_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} + {self.type}'


RECEIVED_CHOICES = [
    ('R', "Received"),
    ('N', "Not Received Yet"),
]


class PurchaseOrder(models.Model):
    date = models.DateTimeField(validators=[MinValueValidator(datetime.date.today)])
    reference = models.CharField(max_length=250)
    total = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name='purchaseorders')
    status = models.CharField(choices=RECEIVED_CHOICES, max_length=250)
    attachment = models.FileField(upload_to='media', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}/{self.date}/{self.supplier}'


class PurchaseOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='purchaseorderitems')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING, related_name='purchaseorderitems')
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product}-{self.created_on}'


class Expense(models.Model):
    date = models.DateTimeField(validators=[MinValueValidator(datetime.date.today)])
    reference = models.CharField(max_length=250)
    amount = models.IntegerField()
    attachment = models.FileField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}-{self.amount}-{self.created_on}'
