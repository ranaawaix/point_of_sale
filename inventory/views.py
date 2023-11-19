import datetime

from django.db.models import Sum
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from POS.models import Product
from inventory.forms import AddCategoriesForm, AddPurchaseOrderForm, PurchaseOrderItemForm, AddExpenseForm, AddSupplierForm
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
        purchase_order_id = self.request.POST.get('po_id')
        if not purchase_order_id:
            purchase_order = PurchaseOrder(total=0, date=datetime.datetime.now())
            purchase_order.save()
        else:
            purchase_order = get_object_or_404(PurchaseOrder.objects.filter(id=purchase_order_id))
        prod_id = self.request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        po_item = PurchaseOrderItem.objects.filter(product=product, purchase_order=purchase_order).first()
        po_item = po_item if po_item else PurchaseOrderItem(product_id=prod_id, purchase_order=purchase_order, price=0,
                                                            quantity=1, total=0)
        po_item.price = product.price
        po_item.total = po_item.quantity * po_item.price
        po_item.save()
        purchase_order.total = \
            purchase_order.purchaseorderitems.filter(purchase_order=purchase_order).aggregate(total=Sum('total'))[
                'total']
        purchase_order.save()
        initial_data = []
        for purchase_order_item in purchase_order.purchaseorderitems.all():
            initial_data.append({'quantity': purchase_order_item.quantity, 'price': purchase_order_item.price})
        PurchaseOrderItemFormSet = modelformset_factory(PurchaseOrderItem, form=PurchaseOrderItemForm, can_delete=True,
                                                        extra=0, error_messages=False, )
        context = self.get_context_data(
            **{'purchase_order': purchase_order, 'item': po_item, 'form': AddPurchaseOrderForm(request.POST),
               'purchase_order_item_formset': PurchaseOrderItemFormSet(initial=initial_data)})
        return self.render_to_response(context)


class EditPurchaseOrderItem(TemplateView):
    template_name = 'inventory/includes/purchase_item_include.html'

    def post(self, request, *args, **kwargs):
        purchase_order_id = request.POST.get('po_id')
        prod_id = request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        purchase_order_item = PurchaseOrderItem.objects.get(purchase_order=purchase_order, product=product)
        purchase_order_item.quantity = request.POST.get('quantity')
        purchase_order_item.price = request.POST.get('price')
        purchase_order_item.total = request.POST.get('subtotal')
        purchase_order_item.save()
        return HttpResponse(self.template_name)


class DeletePurchaseItem(TemplateView):
    template_name = 'inventory/includes/purchase_item_include.html'

    def post(self, request, *args, **kwargs):
        purchase_order_id = request.POST.get('po_id')
        purchase_order_item_id = request.POST.get('item_id')
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        po_item = PurchaseOrderItem.objects.get(purchase_order=purchase_order, id=purchase_order_item_id)
        po_item.delete()
        initial_data = []
        for purchase_order_item in purchase_order.purchaseorderitems.all():
            initial_data.append({'quantity': purchase_order_item.quantity, 'price': purchase_order_item.price})
        PurchaseOrderItemFormSet = modelformset_factory(PurchaseOrderItem, form=PurchaseOrderItemForm, can_delete=True,
                                                        extra=0, error_messages=False, )
        context = self.get_context_data(
            **{'purchase_order': purchase_order, 'item': po_item, 'form': AddPurchaseOrderForm(request.POST),
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
