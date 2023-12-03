from django.contrib import admin
from POS.models import Customer, Store, StoreProduct, Sale, SaleItem, Payment, Hold, Register


# Register your models here.

class ProductInline(admin.TabularInline):
    model = StoreProduct
    extra = 1


class SaleInline(admin.TabularInline):
    model = SaleItem
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class HoldInline(admin.TabularInline):
    model = Hold
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'customer_custom_field_1', 'customer_custom_field_2']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'logo', 'email', 'phone', 'address', 'country', 'city', 'postal_code',
                    'receipt_header', 'receipt_footer', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ('city',)


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'store_price', 'quantity']
    search_fields = ['product', 'store']
    list_filter = ('product', 'store')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['total_items', 'total_price', 'discount', 'order_tax', 'total_payable', 'customer', 'status',
                    'created_at', 'updated_at']
    inlines = [SaleInline, PaymentInline, HoldInline]
    list_filter = ('status', 'customer')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'sale', 'price', 'quantity', 'total', 'created_at', 'updated_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['sale', 'note', 'amount', 'payment_by', 'payment_note', 'created_at', 'updated_at']


@admin.register(Hold)
class HoldAdmin(admin.ModelAdmin):
    list_display = ['reference_note', 'sale']


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'opening_cash_in_hand', 'closing_cash_in_hand', 'status', 'created_on', 'updated_on']


admin.site.site_header = "SimplePOS"
admin.site.site_title = "My SimplePOS Site"
