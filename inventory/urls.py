from django.urls import path
from inventory import views

urlpatterns = [
    path('list_categories', views.ListCategoriesView.as_view(), name='list-categories'),
    path('add_category', views.AddCategory.as_view(), name='add-category'),
    path('update_category/<int:pk>', views.UpdateCategoryView.as_view(), name='update-category'),
    path('delete_category/<int:pk>', views.DeleteCategoryView.as_view(), name='delete-category'),
    path('add_purchase_order', views.AddPurchaseView.as_view(), name='add-purchase-order'),
    path('list_purchase_orders', views.PurchaseOrderListView.as_view(), name='list-purchase-orders'),
    path('add_purchase_order_item/<int:prod_id>', views.AddPurchaseOrderItemView.as_view(), name='add-purchase-order-item'),
    path('edit_purchase_order', views.EditPurchaseOrderItem.as_view(), name='edit-purchase-order'),
    path('delete_purchase_order_item', views.DeletePurchaseItem.as_view(), name='delete-purchase-order-item'),
    path('add_expense', views.AddExpenseView.as_view(), name='add-expense'),
    path('list_expenses', views.ListExpensesView.as_view(), name='list-expenses'),
    path('update_expense/<int:pk>', views.EditExpense.as_view(), name='edit-expense'),
    path('delete_expense/<int:pk>', views.DeleteExpense.as_view(), name='delete-expense'),
    path('add_supplier', views.AddSuplierView.as_view(), name='add-supplier'),
    path('list_suppliers', views.SupplierListView.as_view(), name='list-suppliers'),
    path('update_supplier/<int:pk>', views.UpdateSupplierView.as_view(), name='edit-supplier'),
    path('delete_supplier/<int:pk>', views.DeleteSupplierView.as_view(), name='delete-supplier'),

]