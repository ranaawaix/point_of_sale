from inventory.models import Category, PurchaseOrder, PurchaseOrderItem, Expense, Supplier
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['image', 'code', 'name']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Category.objects.create(**validated_data)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['date', 'reference', 'total', 'supplier', 'status', 'attachment', 'note']


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'price', 'total']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['date', 'reference', 'amount', 'attachment', 'note']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Expense.objects.create(**validated_data)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'supplier_custom_field_1', 'supplier_custom_field_2']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Supplier.objects.create(**validated_data)
