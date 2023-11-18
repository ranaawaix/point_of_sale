from django.contrib import admin
from inventory.models import Supplier, ProductType, Barcode, Category, Product, PurchaseOrder, PurchaseOrderItem, \
    Expense
from POS.admin import ProductInline


# Register your models here.


class SupplierInline(admin.TabularInline):
    model = Supplier
    extra = 1


class ProductTypeInline(admin.TabularInline):
    model = ProductType
    extra = 1


class BarcodeInline(admin.TabularInline):
    model = Barcode
    extra = 1


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'supplier_custom_field_1', 'supplier_custom_field_2']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


# @admin.register(Barcode)
# class BarcodeAdmin(admin.ModelAdmin):
#     list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'image']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'type', 'barcode_symbology', 'category', 'cost', 'price', 'product_tax',
                    'tax_method', 'alert_quantity', 'image', 'details', 'created_on', 'modified_on']
    # exclude = ['quantity']
    inlines = [ProductInline]
    search_fields = ['name']
    list_filter = ('type', 'category', 'tax_method')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'reference', 'total', 'supplier', 'status', 'attachment', 'note', 'created_on',
                    'modified_on']
    inlines = [PurchaseOrderItemInline]
    search_fields = ['supplier']
    list_filter = ('supplier', 'date')


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'purchase_order', 'price', 'quantity', 'total', 'created_on', 'modified_on']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'reference', 'amount', 'attachment', 'note', 'created_on', 'modified_on']
    list_filter = ('date',)
