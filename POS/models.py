from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from inventory.models import Product


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.PositiveIntegerField(validators=[MaxValueValidator(99999999999)], null=True, blank=True)
    customer_custom_field_1 = models.CharField(max_length=250, null=True, blank=True)
    customer_custom_field_2 = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.id}-{self.name}'


class Store(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    logo = models.ImageField(null=True, blank=True)
    email = models.EmailField()
    phone = models.IntegerField(validators=[MaxValueValidator(99999999999)], null=True, blank=True)
    address = models.TextField()
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.IntegerField(validators=[MaxValueValidator(99999)], null=True, blank=True)
    receipt_header = models.TextField(null=True, blank=True)
    receipt_footer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.code}'


class StoreProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storeproducts')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='storeproducts')
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product}-{self.store}'


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


SALE_STATUS_CHOICES = [
    ('H', 'Held'),
    ('P', 'Paid'),
]


class Sale(models.Model):
    total_items = models.IntegerField()
    total_price = models.IntegerField()
    discount = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                   validators=PERCENTAGE_VALIDATOR)
    order_tax = models.FloatField(null=True, blank=True)
    total_payable = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='sales')
    status = models.CharField(choices=SALE_STATUS_CHOICES, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}-{self.customer}'


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='saleitems')
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING, related_name='saleitems')
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}-{self.product}'


PAYMENT_CHOICES = [
    ('Ca', 'Cash'),
    ('Ch', 'Cheque'),
    ('Cd', 'Card'),
    ('Ep', 'Easy-Paisa'),
]


class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.DO_NOTHING, related_name='payments')
    note = models.TextField(null=True, blank=True)
    amount = models.IntegerField()
    payment_by = models.CharField(choices=PAYMENT_CHOICES, max_length=250)
    payment_note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}-{self.amount}-{self.created_at}'


class Hold(models.Model):
    reference_note = models.TextField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='holds')

    def __str__(self):
        return f'{self.id}-{self.sale.customer}'
