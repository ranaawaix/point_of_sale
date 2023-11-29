import datetime

from django.views.generic.edit import DeletionMixin

from user_accounts.models import User
from django.db.models import Sum
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from POS.models import Product
from inventory.forms import AddCategoriesForm, AddPurchaseOrderForm, PurchaseOrderItemForm, AddExpenseForm, \
    AddSupplierForm
from inventory.models import Category, PurchaseOrder, PurchaseOrderItem, Supplier, Expense


# Create your views here.


class ListCategoriesView(ListView):
    model = Category
    template_name = 'inventory/list_categories.html'
    context_object_name = 'categories'
    paginate_by = 5


class AddCategory(CreateView):
    model = Category
    form_class = AddCategoriesForm
    template_name = 'inventory/add_category.html'
    success_url = reverse_lazy('list-categories')

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        image = request.POST.get('image')
        code = request.POST.get('code')
        name = request.POST.get('name')
        category = Category(user=user, image=image, code=code, name=name)
        category.save()
        return redirect(self.success_url)


class UpdateCategoryView(UpdateView):
    model = Category
    form_class = AddCategoriesForm
    template_name = 'inventory/update_category.html'
    success_url = reverse_lazy('list-categories')


class DeleteCategoryView(DeleteView):
    model = Category
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('list-categories')


class AddPurchaseView(CreateView):
    model = PurchaseOrder
    form_class = AddPurchaseOrderForm
    template_name = 'inventory/add_purchase.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_order_item_formset = self.get_purchase_order_item_formset()
        context['purchase_order_item_formset'] = purchase_order_item_formset
        return context

    def get_purchase_order_item_formset(self):
        PurchaseOrderItemFormSet = modelformset_factory(PurchaseOrderItem, form=PurchaseOrderItemForm, can_delete=True,
                                                        extra=0, error_messages=False, )
        if self.request.POST:
            return PurchaseOrderItemFormSet(self.request.POST)
        else:
            return PurchaseOrderItemFormSet()

    def post(self, request, *args, **kwargs):
        po_id = request.POST.get('po_id')
        purchase_order = PurchaseOrder.objects.get(id=po_id)
        user = request.user
        purchase_order.user = user
        purchase_order.date = request.POST.get('date')
        purchase_order.reference = request.POST.get('reference')
        supplier_id = request.POST.get('supplier')
        supplier = Supplier.objects.get(id=supplier_id)
        purchase_order.supplier = supplier
        purchase_order.status = request.POST.get('status')
        purchase_order.attachment = request.POST.get('attachment')
        purchase_order.note = request.POST.get('note')
        purchase_order.save()
        return redirect('list-categories')


class AddPurchaseOrderItemView(TemplateView):
    template_name = 'inventory/includes/purchase_item_include.html'

    def post(self, request, *args, **kwargs):
        po_id = self.request.POST.get('po_id')
        user = request.user
        prod_id = self.request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        empty_purchase_order = PurchaseOrder(user=user, total=0, date=datetime.datetime.now())
        purchase_order = empty_purchase_order.add_purchase_order(request=request, po_id=po_id, product=product,
                                                                 user=user)
        initial_data = []
        for purchase_order_item in purchase_order.purchaseorderitems.all():
            initial_data.append({'quantity': purchase_order_item.quantity, 'price': purchase_order_item.price})
        PurchaseOrderItemFormSet = modelformset_factory(PurchaseOrderItem, form=PurchaseOrderItemForm, can_delete=True,
                                                        extra=0, error_messages=False, )
        context = self.get_context_data(
            **{'purchase_order': purchase_order, 'form': AddPurchaseOrderForm(request.POST),
               'purchase_order_item_formset': PurchaseOrderItemFormSet(initial=initial_data)})
        return self.render_to_response(context)


class EditPurchaseOrderItem(TemplateView):
    template_name = 'inventory/includes/purchase_item_include.html'

    def post(self, request, *args, **kwargs):
        purchase_order_id = request.POST.get('po_id')
        user = request.user
        prod_id = request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        empty_purchase_order = PurchaseOrder(user=user, total=0, date=datetime.datetime.now())
        purchase_order = empty_purchase_order.add_purchase_order(request=request, po_id=purchase_order_id,
                                                                 product=product, user=user)
        initial_data = []
        for purchase_order_item in purchase_order.purchaseorderitems.all():
            initial_data.append({'quantity': purchase_order_item.quantity, 'price': purchase_order_item.price})
        PurchaseOrderItemFormSet = modelformset_factory(PurchaseOrderItem, form=PurchaseOrderItemForm, can_delete=True,
                                                        extra=0, error_messages=False, )
        context = self.get_context_data(
            **{'purchase_order': purchase_order, 'form': AddPurchaseOrderForm(request.POST),
               'purchase_order_item_formset': PurchaseOrderItemFormSet(initial=initial_data)})
        return self.render_to_response(context)


class DeletePurchaseItem(DeletionMixin, TemplateView):
    template_name = 'inventory/includes/purchase_item_include.html'
    success_url = reverse_lazy('add-purchase-order')

    def post(self, request, *args, **kwargs):
        purchase_order_id = request.POST.get('po_id')
        purchase_order_item_id = request.POST.get('item_id')
        user = request.user
        empty_purchase_order = PurchaseOrder(user=user, total=0, date=datetime.datetime.now())
        purchase_order = empty_purchase_order.delete_purchase_order(po_id=purchase_order_id,
                                                                    item_id=purchase_order_item_id)
        initial_data = []
        for purchase_order_item in purchase_order.purchaseorderitems.all():
            initial_data.append({'quantity': purchase_order_item.quantity, 'price': purchase_order_item.price})
        PurchaseOrderItemFormSet = modelformset_factory(PurchaseOrderItem, form=PurchaseOrderItemForm, can_delete=True,
                                                        extra=0, error_messages=False, )
        context = self.get_context_data(
            **{'purchase_order': purchase_order, 'form': AddPurchaseOrderForm(request.POST),
               'purchase_order_item_formset': PurchaseOrderItemFormSet(initial=initial_data)})
        return self.render_to_response(context)


# class UpdatePurchaseOrderView(UpdateView):
#     model = PurchaseOrder
#     form_class = AddPurchaseOrderForm
#     template_name = 'inventory/add_purchase.html'


# class DeletePurchaseOrderView(DeleteView):
#     model = PurchaseOrder


class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = 'inventory/list_purchase_orders.html'
    context_object_name = 'purchase_orders'
    paginate_by = 5


class AddExpenseView(CreateView):
    model = Expense
    form_class = AddExpenseForm
    template_name = 'inventory/add_expense.html'
    success_url = reverse_lazy('list-expenses')


class ListExpensesView(ListView):
    model = Expense
    template_name = 'inventory/list_expenses.html'
    context_object_name = 'expenses'
    paginate_by = 5


class EditExpense(UpdateView):
    model = Expense
    form_class = AddExpenseForm
    template_name = 'inventory/update_expense.html'


class DeleteExpense(DeleteView):
    model = Expense
    template_name = 'inventory/confirm_delete_expense.html'
    success_url = reverse_lazy('list-expenses')


class AddSuplierView(CreateView):
    model = Supplier
    form_class = AddSupplierForm
    template_name = 'inventory/add_supplier.html'
    success_url = reverse_lazy('list-suppliers')

    def post(self, request, *args, **kwargs):
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cust_1 = request.POST.get('supplier_custom_field_1')
        cust_2 = request.POST.get('supplier_custom_field_2')
        supplier = Supplier(user=user, name=name, email=email, phone=phone, supplier_custom_field_1=cust_1,
                            supplier_custom_field_2=cust_2)
        supplier.save()
        return redirect(reverse_lazy('list-suppliers'))


class SupplierListView(ListView):
    model = Supplier
    template_name = 'inventory/list_suppliers.html'
    context_object_name = 'suppliers'


class UpdateSupplierView(UpdateView):
    model = Supplier
    form_class = AddSupplierForm
    template_name = 'inventory/update_supplier.html'


class DeleteSupplierView(DeleteView):
    model = Supplier
    template_name = 'inventory/confirm_delete_supplier.html'
