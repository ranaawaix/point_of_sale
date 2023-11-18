from inventory.models import Category, PurchaseOrder, PurchaseOrderItem, Expense, Supplier
from django import forms


class AddCategoriesForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['image', 'code', 'name']
        widgets = {'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                   'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code of the Category'}),
                   'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the Category'}), }


class AddPurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['date', 'reference', 'total', 'supplier', 'status', 'attachment', 'note']
        widgets = {'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
                   'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Purchase Reference'}),
                   'supplier': forms.Select(attrs={'class': 'form-control'}),
                   'status': forms.Select(attrs={'class': 'form-control'}),
                   'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                   'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note about the purchase'}), }


class PurchaseOrderItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'price', 'total']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Search by product name'})
        }


class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'reference', 'amount', 'attachment', 'note']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expense Reference'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Expense Amount'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Expense Receipt'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Expense Reason'}),
        }


class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'supplier_custom_field_1', 'supplier_custom_field_2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Supplier email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier phone'}),
            'supplier_custom_field_1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Supplier custom field 1'}),
            'supplier_custom_field_2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Supplier custom field 2'}),
        }
