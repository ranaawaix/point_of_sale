import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from inventory.models import Product
from user_accounts.models import User


# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=250, default='Walk-in Client')
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    customer_custom_field_1 = models.CharField(max_length=250, null=True, blank=True)
    customer_custom_field_2 = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    user = models.ManyToManyField(User, related_name='stores')
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    logo = models.ImageField(null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=250, null=True, blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
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

    def change_sale(self, request, product, quantity, sale_id=None, action=None):
        user = User.objects.get(id=request.user.id)
        register = Register.objects.filter(user=user, status='O').first()
        if not sale_id:
            sale = Sale(total_items=0, user=user)
            sale.save()
        else:
            sale = get_object_or_404(Sale.objects.filter(id=sale_id))
        item = sale.saleitems.filter(sale=sale, product=product).first()
        item = item if item else SaleItem(sale=sale, product=product)
        item.register = register
        if action == '+':
            item.quantity += quantity
        elif action == '-':
            item.quantity -= quantity
        else:
            item.quantity = quantity
        item.price = product.price
        item.total = item.quantity * product.price
        item.save()
        sale.user = user
        sale.total_items = sale.saleitems.count()
        sale.total_price = sale.saleitems.filter(sale=sale).aggregate(total_price=Sum('total'))['total_price']
        sale.total_payable = (sale.total_price + sale.order_tax) - sale.discount
        sale.save()
        if sale.saleitems.count() != 0:
            sale.total_items = sale.saleitems.count()
            sale.total_price = sale.saleitems.filter(sale=sale).aggregate(total_price=Sum('total'))['total_price']
            sale.total_payable = (sale.total_price + sale.order_tax) - sale.discount
            sale.save()
        else:
            sale.delete_sale(sale_id=sale_id)
        return sale

    def add_sale(self, request, product, sale_id=None, quantity=1):
        return self.change_sale(request, product, quantity, sale_id, '+')

    def subtract_sale(self, request, product, sale_id=None, quantity=1):
        return self.change_sale(request, product, quantity, sale_id, '-')

    def delete_sale(self, sale_id):
        sale = Sale.objects.get(id=sale_id)
        sale.delete()

    def delete_sale_item(self, sale_id, sale_item_id):
        sale = Sale.objects.get(id=sale_id)
        item = sale.saleitems.get(sale=sale, product_id=sale_item_id)
        item.delete()
        if sale.saleitems.count() != 0:
            sale.total_items = sale.saleitems.count()
            sale.total_price = sale.saleitems.filter(sale=sale).aggregate(total_price=Sum('total'))['total_price']
            sale.total_payable = (sale.total_price + sale.order_tax) - sale.discount
            sale.save()
        else:
            sale.delete_sale(sale_id=sale_id)
        return sale


REGISTER_STATUS_CHOICES = [
    ('O', 'Open'),
    ('C', 'Close'),
]


class Register(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='pos')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pos')
    opening_cash_in_hand = models.IntegerField(null=True, blank=True)
    closing_cash_in_hand = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=REGISTER_STATUS_CHOICES ,max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.store} - {self.user}'


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saleitems')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='saleitems')
    register = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='saleitems')
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
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
