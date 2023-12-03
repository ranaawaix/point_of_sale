from django import forms
from django.forms import inlineformset_factory

from POS.models import Sale, SaleItem, Hold, Customer, Payment, Store, StoreProduct, Register
from inventory.models import Product


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'total_items', 'total_price', 'discount', 'order_tax', 'total_payable']
        widgets = {'customer': forms.Select(attrs={'class': 'form-control', 'default': 'Walk-in Client'}), }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'price', 'quantity', 'total']
        widgets = {'product': forms.Select(attrs={'class': 'form-control w-10'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control w-8'}),
                   'quantity': forms.NumberInput(attrs={'class': 'form-control w-8'}),
                   'total': forms.NumberInput(attrs={'class': 'form-control w-8'}), }


class HoldOrderForm(forms.ModelForm):
    class Meta:
        model = Hold
        fields = ['reference_note']
        widgets = {'reference_note': forms.Textarea(attrs={'class': 'form-control'}), }


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'customer_custom_field_1', 'customer_custom_field_2']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Customer Email'}),
                   'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Phone'}),
                   'customer_custom_field_1': forms.Textarea(
                       attrs={'class': 'form-control', 'placeholder': 'Customer Extra Detail 1'}),
                   'customer_custom_field_2': forms.Textarea(
                       attrs={'class': 'form-control', 'placeholder': 'Customer Extra Detail 2'}), }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['note', 'amount', 'payment_by', 'payment_note']
        widgets = {'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note'}),
                   'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Payment Amount'}),
                   'payment_by': forms.Select(attrs={'class': 'form-control'}),
                   'payment_note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Payment Note'}), }


class AddStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'code', 'logo', 'email', 'phone', 'address', 'city', 'country', 'postal_code',
                  'receipt_header', 'receipt_footer']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Store Name'}),
                   'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Store Code'}),
                   'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Store Email'}),
                   'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Store Phone'}),
                   'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Store Address'}),
                   'city': forms.Select(attrs={'class': 'form-control'}),
                   'country': forms.Select(attrs={'class': 'form-control'}), 'postal_code': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Store Postal Code'}), 'receipt_header': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Receipt Header Text'}),
                   'receipt_footer': forms.Textarea(
                       attrs={'class': 'form-control', 'placeholder': 'Receipt Footer Text'}), }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['type', 'name', 'code', 'barcode_symbology', 'category', 'cost', 'price', 'product_tax', 'tax_method',
                  'alert_quantity', 'image', 'details']
        exclude = ['quantity']
        widgets = {'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Code'}),
            'barcode_symbology': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost of the Product'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price of the Product'}),
            'product_tax': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tax of the Product'}),
            'tax_method': forms.Select(attrs={'class': 'form-control'}),
            'alert_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Alert Quantity of the '
                                                                                               'Product'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}), 'details': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Any other details of the Product'}), }


class StoreProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.store_info = kwargs['initial']['store']
        kwargs['initial']['store'] = self.store_info.id
        super().__init__(*args, **kwargs)

    class Meta:
        model = StoreProduct
        fields = ['store', 'store_price', 'quantity']
        exclude = ['product', 'id']
        widgets = {'store_price': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Price of the Product in this store'}),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Quantity of the Product in this store'}),
            'store': forms.HiddenInput(), }


class CashInHandForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['opening_cash_in_hand']
        widgets = {'opening_cash_in_hand': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Opening cash in hand'}), }
