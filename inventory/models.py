import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from user_accounts.models import User


# Create your models here.

class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    supplier_custom_field_1 = models.CharField(max_length=250, null=True, blank=True)
    supplier_custom_field_2 = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    code = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
TAX_CHOICES = [
    ('In', 'Inclusive'),
    ('Ex', 'Exclusive'),
]


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    barcode_symbology = models.ForeignKey(Barcode, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    cost = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    quantity = models.IntegerField(null=True, blank=True)
    product_tax = models.DecimalField(max_digits=3, decimal_places=0, default=0,
                                      validators=PERCENTAGE_VALIDATOR)
    tax_method = models.CharField(max_length=250, choices=TAX_CHOICES)
    alert_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


RECEIVED_CHOICES = [
    ('R', "Received"),
    ('N', "Not Received Yet"),
]


class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchaseorders')
    date = models.DateTimeField()
    reference = models.CharField(max_length=250, null=True, blank=True)
    total = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchaseorders', null=True,
                                 blank=True)
    status = models.CharField(choices=RECEIVED_CHOICES, max_length=250, default='N')
    attachment = models.FileField(upload_to='media', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'

    def add_purchase_order(self, request, product, user, po_id=None):
        if not po_id:
            purchase_order = PurchaseOrder(user=user, total=0, date=datetime.datetime.now())
            purchase_order.save()
        else:
            purchase_order = get_object_or_404(PurchaseOrder.objects.filter(id=po_id))
        po_item = PurchaseOrderItem.objects.filter(product=product, purchase_order=purchase_order).first()
        po_item = po_item if po_item else PurchaseOrderItem(product=product, purchase_order=purchase_order,
                                                            price=0,
                                                            quantity=0, total=0)
        if request.POST.get('quantity'):
            po_item.quantity = int(request.POST.get('quantity'))
            po_item.price = int(request.POST.get('price'))
            po_item.total = po_item.quantity * po_item.price
            po_item.save()
        else:
            po_item.quantity += 1
            po_item.price = product.price
            po_item.total = po_item.quantity * po_item.price
            po_item.save()
        purchase_order.total = \
            purchase_order.purchaseorderitems.filter(purchase_order=purchase_order).aggregate(total=Sum('total'))[
                'total']
        purchase_order.save()
        if purchase_order.purchaseorderitems.count() != 0:
            purchase_order.total = \
                purchase_order.purchaseorderitems.filter(purchase_order=purchase_order).aggregate(
                    total=Sum('total'))[
                    'total']
            purchase_order.save()
        else:
            purchase_order.delete()
        return purchase_order

    def delete_purchase_order(self,item_id, po_id):
        purchase_order = PurchaseOrder.objects.get(id=po_id)
        item = purchase_order.purchaseorderitems.get(id=item_id)
        item.delete()
        if purchase_order.purchaseorderitems.count() != 0:
            purchase_order.total = \
                purchase_order.purchaseorderitems.filter(purchase_order=purchase_order).aggregate(
                    total=Sum('total'))[
                    'total']
            purchase_order.save()
        else:
            purchase_order.total = \
                purchase_order.purchaseorderitems.filter(purchase_order=purchase_order).aggregate(
                    total=Sum('total'))[
                    'total']
            purchase_order.delete()
        return purchase_order

    class Meta:
        verbose_name_plural = 'Purchase Orders'


class PurchaseOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchaseorderitems')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='purchaseorderitems')
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name}'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date = models.DateTimeField()
    reference = models.CharField(max_length=250)
    amount = models.IntegerField()
    attachment = models.FileField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.reference}-{self.amount}'
