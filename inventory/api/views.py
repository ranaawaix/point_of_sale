from rest_framework import viewsets
from inventory.models import Category, PurchaseOrder, PurchaseOrderItem, Supplier, Expense
from inventory.api.serializers import CategoriesSerializer, SupplierSerializer, ExpenseSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CategoriesAPIViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    # pagination_class = [PageNumberPagination]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class SuppliersAPIViewset(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    # pagination_class = [PageNumberPagination]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseAPIViewset(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    # pagination_class = [PageNumberPagination]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]