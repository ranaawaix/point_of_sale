from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from inventory.models import Product


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    customer_custom_field_1 = models.CharField(max_length=250, null=True, blank=True)
    customer_custom_field_2 = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    logo = models.ImageField(null=True, blank=True)
    email = models.EmailField()
    phone = models.BigIntegerField(null=True, blank=True)
    address = models.TextField()
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.IntegerField(validators=[MaxValueValidator(99999)], null=True, blank=True)
    receipt_header = models.TextField(null=True, blank=True)
    receipt_footer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storeproducts')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='storeproducts')
    store_price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ['product', 'store']

    def __str__(self):
        return f'{self.product}-{self.store}'


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


SALE_STATUS_CHOICES = [
    ('H', 'Held'),
    ('P', 'Paid'),
]


class Sale(models.Model):
    total_items = models.IntegerField()
    total_price = models.IntegerField(null=True, blank=True, default=0)
    discount = models.IntegerField(default=0)
    order_tax = models.IntegerField(null=True, blank=True, default=0)
    total_payable = models.IntegerField(null=True, blank=True, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales', default=27)
    status = models.CharField(choices=SALE_STATUS_CHOICES, max_length=250, default='H')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.name


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saleitems')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='saleitems')
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


PAYMENT_CHOICES = [
    ('Ca', 'Cash'),
    ('Ch', 'Cheque'),
    ('Cd', 'Card'),
    ('Ep', 'Easy-Paisa'),
]


class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    note = models.TextField(null=True, blank=True)
    amount = models.IntegerField()
    payment_by = models.CharField(choices=PAYMENT_CHOICES, max_length=250, default='Ca')
    payment_note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)


class Hold(models.Model):
    reference_note = models.TextField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='holds')

    def __str__(self):
        return self.reference_note
