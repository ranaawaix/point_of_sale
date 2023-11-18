from django.urls import path
from POS import views

urlpatterns = [
    path('stores', views.StoreListView.as_view(), name='stores'),
    path('create_sale', views.POS.as_view(), name='create-sale'),
    path('update_sale/<int:pk>', views.POSUpdateView.as_view(), name='update-sale'),
    path('delete_sale/<int:pk>', views.POSDeleteView.as_view(), name='delete-sale'),
    path('create_customer', views.AddCustomerView.as_view(), name='create-customer'),
    path('create_payment', views.PaymentView.as_view(), name='create-payment'),
    path('hold_sale', views.HoldOrderView.as_view(), name='hold-sale'),
    path('delete_saleitem', views.DeleteSaleItemView.as_view(), name='delete-saleitem'),
    path('create_sale/<int:prod_id>', views.SaleView.as_view(), name='create-sale-product'),
    path('create_store', views.AddStoreView.as_view(), name='create-store'),
    path('add_customer', views.AddCustomersView.as_view(), name='add-customer'),
    path('list_customers', views.ListCustomersView.as_view(), name='list-customers'),
    path('update_customer/<int:pk>', views.UpdateCustomerView.as_view(), name='update-customer'),
    path('delete_customer/<int:pk>', views.DeleteCustomerView.as_view(), name='delete-customer'),
    path('list_products', views.ProductListView.as_view(), name='list-products'),
    path('add_product', views.AddProductView.as_view(), name='add-product'),
    path('update_product/<int:pk>', views.UpdateProductView.as_view(), name='update-product'),
    path('delete_product/<int:pk>', views.DeleteProductView.as_view(), name='delete-product'),
    path('list_products/<int:pk>', views.StoreWiseProductListView.as_view(), name='list-products-by-store'),
    path('list_sales', views.SaleListView.as_view(), name='list-sales'),
    path('list_opened_bills', views.OpenedBillsView.as_view(), name='list-opened-bills'),
]