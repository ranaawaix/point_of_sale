import calendar
import datetime
from cities_light.models import City, Country
from django.contrib import messages
from django.db.models import Sum
from django.forms.models import inlineformset_factory, modelformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from POS.forms import SaleForm, HoldOrderForm, AddCustomerForm, PaymentForm, AddStoreForm, AddProductForm, \
    StoreProductForm, CashInHandForm, SaleReportFilterForm, PaymentReportFilterForm, RegistersReportFilterForm, \
    ProductsReportFilterForm
from POS.models import Sale, Hold, Customer, Payment, Register, SaleItem
from POS.models import Store, StoreProduct
from inventory.models import Product, PurchaseOrder, Expense
from user_accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class StoreListView(LoginRequiredMixin, ListView):
    model = Store
    template_name = 'POS/list_stores.html'
    context_object_name = 'stores'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if user.group == 'A':
            self.queryset = Store.objects.all()
        else:
            self.queryset = Store.objects.filter(user=user)
        return self.queryset


class POS(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'POS/pos.html'
    success_url = reverse_lazy('stores')

    def get_context_data(self, *args, **kwargs):
        store_id = self.kwargs['store_id']
        register_id = self.kwargs['register_id']
        context = super().get_context_data(**kwargs)
        store = Store.objects.get(id=store_id)
        context['storeproducts'] = StoreProduct.objects.filter(store=store)
        context['register'] = Register.objects.get(id=register_id)
        context['holdform'] = HoldOrderForm(self.request.POST)
        context['customerform'] = AddCustomerForm(self.request.POST)
        context['paymentform'] = PaymentForm(self.request.POST)
        return context

    def get(self, request, *args, **kwargs):
        register_id = kwargs['register_id']
        register = Register.objects.get(id=register_id)
        if register:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Please open the register to access POS')
            return redirect(reverse_lazy('cash-in-hand'))


class SaleView(LoginRequiredMixin, TemplateView):
    template_name = 'includes/pos_include.html'

    def post(self, request, prod_id):
        sale_id = self.request.POST.get('sale_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        empty_sale = Sale(user=user, total_items=0, total_price=0)
        sale = empty_sale.add_sale(request=request, product=product, sale_id=sale_id)
        context = self.get_context_data(
            **{'sale': sale, 'form': SaleForm(request.POST), 'holdform': HoldOrderForm(request.POST),
               'customerform': AddCustomerForm(request.POST), 'paymentform': PaymentForm(request.POST)})
        return self.render_to_response(context)


class SaleItemUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'includes/pos_include.html'

    def post(self, request, *args, **kwargs):
        prod_id = request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        sale_id = self.request.POST.get('sale_id')
        quantity = int(request.POST.get('quantity'))
        current_sale = Sale(id=sale_id)
        sale = current_sale.change_sale(request=request, product=product, quantity=quantity, sale_id=sale_id)
        context = self.get_context_data(
            **{'sale': sale, 'form': SaleForm(request.POST), 'holdform': HoldOrderForm(request.POST),
               'customerform': AddCustomerForm(request.POST), 'paymentform': PaymentForm(request.POST)})
        return self.render_to_response(context)


class HoldOrderView(LoginRequiredMixin, CreateView):
    model = Hold
    form_class = HoldOrderForm
    success_url = reverse_lazy('list-opened-bills')

    def post(self, request, *args, **kwargs):
        sale_id = request.POST.get('sale_id')
        sale = Sale.objects.get(id=sale_id)
        note = request.POST.get('note')
        hold = Hold.objects.create(sale=sale, reference_note=note)
        hold.save()
        if hold:
            sale.status = 'H'
            sale.save()
            return JsonResponse({'status': "Saved"})
        else:
            return JsonResponse({'status': 0})


class AddCustomerView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = AddCustomerForm

    def post(self, request, *args, **kwargs):
        sale_id = request.POST.get('sale_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        custom_1 = request.POST.get('custom_1')
        custom_2 = request.POST.get('custom_2')
        customer = Customer(name=name, email=email, phone=phone, customer_custom_field_1=custom_1,
                            customer_custom_field_2=custom_2)
        customer.save()
        customer_id = str(customer.id)
        if sale_id and customer:
            sale = Sale.objects.get(id=sale_id)
            sale.customer = customer
            sale.save()
        if customer:
            return JsonResponse({'status': "Saved", 'cust_id': customer_id})
        else:
            return JsonResponse({'status': 0})


class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('list-sales')

    def post(self, request, *args, **kwargs):
        sale_id = request.POST.get('sale_id')
        if sale_id:
            sale = Sale.objects.get(id=sale_id)
            note = request.POST.get('note')
            amount = int(request.POST.get('amount'))
            payment_by = request.POST.get('payment_by')
            payment_note = request.POST.get('payment_note')
            payment = Payment(sale=sale, note=note, amount=amount, payment_by=payment_by, payment_note=payment_note)
            payment.save()
            sale.status = 'P'
            sale.save()
            return JsonResponse({"status": "Saved"})
        else:
            return JsonResponse({'status': 0})


class DeleteSaleItemView(LoginRequiredMixin, TemplateView):
    template_name = 'includes/pos_include.html'

    def post(self, request, *args, **kwargs):
        sale_id = request.POST.get('sale_id')
        sale_item_id = request.POST.get('saleitem_id')
        sale = get_object_or_404(Sale, id=sale_id)
        sale = sale.delete_sale_item(sale_id=sale_id, sale_item_id=sale_item_id)
        if sale.saleitems.count() == 0:
            sale.delete()
            context = self.get_context_data(**{'form': SaleForm(request.POST), 'holdform': HoldOrderForm(request.POST),
                                               'customerform': AddCustomerForm(request.POST),
                                               'paymentform': PaymentForm(request.POST)})
            return self.render_to_response(context)
        else:
            context = self.get_context_data(
                **{'sale': sale, 'form': SaleForm(request.POST), 'holdform': HoldOrderForm(request.POST),
                   'customerform': AddCustomerForm(request.POST), 'paymentform': PaymentForm(request.POST)})
            return self.render_to_response(context)


class AddStoreView(LoginRequiredMixin, CreateView):
    model = Store
    form_class = AddStoreForm
    template_name = 'POS/add_store.html'
    success_url = reverse_lazy('stores')

    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        name = request.POST.get('name')
        city_id = request.POST.get('city')
        city = City.objects.get(id=city_id)
        country_id = request.POST.get('country')
        country = Country.objects.get(id=country_id)
        postal_code = request.POST.get('postal_code')
        receipt_header = request.POST.get('receipt_header')
        receipt_footer = request.POST.get('receipt_footer')
        code = request.POST.get('code')
        logo = request.POST.get('logo')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        store = Store(name=name, code=code, city=city, country=country, postal_code=postal_code,
                      receipt_header=receipt_header, receipt_footer=receipt_footer, logo=logo, email=email, phone=phone,
                      address=address)
        store.save()
        store.user.add(user)
        return redirect(self.success_url)


class AddCustomersView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = AddCustomerForm
    template_name = 'POS/add_customer.html'
    success_url = reverse_lazy('list-customers')


class ListCustomersView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'POS/list_customers.html'
    context_object_name = 'customers'
    paginate_by = 5


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = AddCustomerForm
    template_name = 'POS/update_customer.html'
    success_url = reverse_lazy('list-customers')


class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'POS/confirm_delete.html'
    success_url = reverse_lazy('list-customers')


class ProductListView(LoginRequiredMixin, ListView):
    model = StoreProduct
    template_name = 'POS/list_products.html'
    context_object_name = 'storeproducts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['stores'] = Store.objects.all()
        return context


class StoreWiseProductListView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    model = StoreProduct
    template_name = 'POS/list_products.html'
    paginate_by = 5

    def get(self, request, pk):
        stores = Store.objects.all()
        store = Store.objects.get(id=pk)
        self.queryset = StoreProduct.objects.filter(store=store)
        return render(request, template_name=self.template_name,
                      context={'stores': stores, 'store': store, 'storeproducts': self.queryset})


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'POS/add_products.html'
    success_url = reverse_lazy('list-products')

    def get_store_product_formset(self):
        """
        Formset for store products.
        """
        stores = Store.objects.all()
        total_stores = len(stores)
        initial_data = []
        for store in stores:
            initial_data.append({'store': store, })
        storeproductset = modelformset_factory(StoreProduct, form=StoreProductForm,
                                               fields=('store', 'store_price', 'quantity'), extra=total_stores,
                                               can_delete=False, )
        if self.request.POST:
            return storeproductset(self.request.POST, initial=initial_data, queryset=StoreProduct.objects.none())
        else:
            return storeproductset(initial=initial_data, queryset=StoreProduct.objects.none())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'storeproductformset' not in kwargs:
            context['storeproductformset'] = self.get_store_product_formset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['storeproductformset']
        if form.is_valid() and formset.is_valid():
            form.instance.user = self.request.user
            self.object = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = self.object
                instance.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    template_name = 'POS/update_products.html'
    success_url = reverse_lazy('list-products')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        parent_instance = StoreProduct.objects.filter(product=self.object)
        initial_data = []
        for instance in parent_instance:
            dict = {'store_price': instance.store_price, 'quantity': instance.quantity, 'store': instance.store}
            initial_data.append(dict)
        context = super().get_context_data(object=self.object)
        context['stores'] = Store.objects.all()
        storeproductset = inlineformset_factory(Store, StoreProduct, StoreProductForm, extra=len(initial_data),
                                                can_delete=False)
        if self.request.POST:
            context['storeproductformset'] = storeproductset(self.request.POST, initial=initial_data)
        else:
            context['storeproductformset'] = storeproductset(initial=initial_data)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        storeproductformset = context['storeproductformset']
        if storeproductformset.is_valid() and form.is_valid():
            self.object = form.save()
            storeproductformset.instance = self.object
            storeproductformset.save()
            return super().form_valid(form)


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'POS/confirm_delete_product.html'
    success_url = reverse_lazy('list-products')


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'POS/list_sales.html'
    queryset = Sale.objects.filter(status='P')
    context_object_name = 'sales'
    paginate_by = 5


class OpenedBillsView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'POS/list_opened_bills.html'
    queryset = Sale.objects.filter(status='H')
    context_object_name = 'sales'
    paginate_by = 5


class POSUpdateView(LoginRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'POS/pos.html'
    success_url = reverse_lazy('list-opened-bills')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        store_id = self.kwargs['store_id']
        store = Store.objects.get(id=store_id)
        context = super().get_context_data(object=self.object)
        context['storeproducts'] = StoreProduct.objects.filter(store=store)
        context['holdform'] = HoldOrderForm(self.request.POST or None, instance=self.object)
        context['customerform'] = AddCustomerForm(self.request.POST or None, instance=self.object)
        context['paymentform'] = PaymentForm(self.request.POST or None, instance=self.object)
        return context


class POSDeleteView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'POS/confirm_delete_sale.html'
    success_url = reverse_lazy('list-opened-bills')


class StoreSelectView(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, store_id):
        stores = Store.objects.all()
        store = Store.objects.get(id=store_id)
        user = request.user
        form = CashInHandForm(self.request.POST)
        user_id = user.id
        store_user_id = user.stores.instance.id
        if user_id == store_user_id:
            selected_store = Register(store=store, user=user, status='O')
            selected_store.save()
            return render(request, template_name='POS/register.html',
                          context={'selected_store': selected_store, 'store': store, 'form': form})
        else:
            messages.error(self.request, 'You are not authorized to enter this store')
            return render(request, template_name='POS/list_stores.html', context={'stores': stores})


class CashInHandView(LoginRequiredMixin, CreateView):
    model = Register
    success_url = reverse_lazy('create-sale')

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        store_id = request.POST.get('store_id')
        store = Store.objects.get(id=store_id)
        register_id = request.POST.get('register_id')
        register = Register.objects.get(id=register_id, user=user, store=store)
        cash_in_hand = request.POST.get('opening_cash_in_hand')
        form = CashInHandForm(self.request.POST)
        if cash_in_hand is not '':
            register.opening_cash_in_hand = cash_in_hand
            register.save()
            return redirect('create-sale', register_id=register_id, store_id=store_id)
        else:
            messages.error(self.request,
                           'Please enter the opening cash in hand amount. Enter "0" if no opening amount.')
            return render(request, template_name='POS/register.html',
                          context={'selected_store': register, 'form': form})


class CloseRegisterView(LoginRequiredMixin, View):

    def post(self, request):
        register_id = request.POST.get('register_id')
        register = Register.objects.get(id=register_id)
        if register.saleitems:
            register.closing_cash_in_hand = \
                register.saleitems.filter(register_id=register_id).aggregate(closing_cash_in_hand=Sum('total'))[
                    'closing_cash_in_hand']
            register.status = 'C'
            register.save()
        else:
            register.closing_cash_in_hand = 0
            register.status = 'C'
            register.save()
        return redirect('stores')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = Sale.objects.filter(created_at__month=datetime.datetime.now().month)
        context['sales'] = sale
        tax = sale.aggregate(Sum('order_tax'))['order_tax__sum']
        context['tax'] = tax
        discount = sale.aggregate(Sum('discount'))['discount__sum']
        context['discount'] = discount
        month = datetime.datetime.now().month
        current_month_name = calendar.month_name[month]
        current_year_name = datetime.datetime.now().year
        display = f'{current_month_name} - {current_year_name}'
        context['month'] = {'display': display}
        products = SaleItem.objects.filter(created_at__month=datetime.datetime.now().month).values(
            'product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
        context['products'] = products
        return context


class DailyReportView(LoginRequiredMixin, TemplateView):
    template_name = 'POS/daily_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sales_value = Sale.objects.filter(status='P', created_at__day=datetime.datetime.today().day).aggregate(
            sales_value=Sum('total_payable'))['sales_value']
        if not sales_value:
            sales_value = 0
        sale_count = Sale.objects.filter(status='P', created_at__day=datetime.datetime.today().day).count()
        context['sales_value'] = sales_value
        context['sale_count'] = sale_count
        purchase_value = PurchaseOrder.objects.filter(modified_on__day=datetime.datetime.today().day).aggregate(
            purchase_value=Sum('total'))['purchase_value']
        if not purchase_value:
            purchase_value = 0
        purchase_count = PurchaseOrder.objects.filter(modified_on__day=datetime.datetime.today().day).count()
        context['purchase_value'] = purchase_value
        context['purchase_count'] = purchase_count
        expense_value = \
            Expense.objects.filter(date__day=datetime.datetime.today().day).aggregate(expense_value=Sum('amount'))[
                'expense_value']
        if not expense_value:
            expense_value = 0
        expense_count = Expense.objects.filter(date__day=datetime.datetime.today().day).count()
        context['expense_value'] = expense_value
        context['expense_count'] = expense_count
        today_cost = \
            SaleItem.objects.filter(updated_at__day=datetime.datetime.today().day).values('product__cost').aggregate(
                Sum('product__cost'))['product__cost__sum']
        if not today_cost:
            today_cost = 0
        profit = sales_value - (today_cost + purchase_value + expense_value)
        context['profit'] = profit
        return context


class MonthlyReportView(LoginRequiredMixin, TemplateView):
    template_name = 'POS/monthly_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sales_value = Sale.objects.filter(status='P', created_at__month=datetime.datetime.today().month).aggregate(
            sales_value=Sum('total_payable'))['sales_value']
        if not sales_value:
            sales_value = 0
        sale_count = Sale.objects.filter(status='P', created_at__month=datetime.datetime.today().month).count()
        context['sales_value'] = sales_value
        context['sale_count'] = sale_count
        purchase_value = PurchaseOrder.objects.filter(modified_on__month=datetime.datetime.today().month).aggregate(
            purchase_value=Sum('total'))['purchase_value']
        if not purchase_value:
            purchase_value = 0
        purchase_count = PurchaseOrder.objects.filter(modified_on__month=datetime.datetime.today().month).count()
        context['purchase_value'] = purchase_value
        context['purchase_count'] = purchase_count
        expense_value = \
            Expense.objects.filter(date__month=datetime.datetime.today().month).aggregate(expense_value=Sum('amount'))[
                'expense_value']
        if not expense_value:
            expense_value = 0
        expense_count = Expense.objects.filter(date__month=datetime.datetime.today().month).count()
        context['expense_value'] = expense_value
        context['expense_count'] = expense_count
        today_cost = \
            SaleItem.objects.filter(updated_at__month=datetime.datetime.today().month).values(
                'product__cost').aggregate(
                Sum('product__cost'))['product__cost__sum']
        if not today_cost:
            today_cost = 0
        profit = sales_value - (today_cost + purchase_value + expense_value)
        context['profit'] = profit
        return context


class SalesReportView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'POS/sales_report.html'
    context_object_name = 'sales'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter_form'] = SaleReportFilterForm(self.request.POST)
        return context


class FilterSalesReportView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    model = Sale
    template_name = 'POS/sales_report.html'
    paginate_by = 5
    context_object_name = 'sales'

    def post(self, request):
        customer_id = request.POST.get('customer')
        sales = Sale.objects.all()
        user_id = request.POST.get('user')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            sales = Sale.objects.filter(customer=customer)
        elif user_id:
            user = User.objects.get(id=user_id)
            sales = Sale.objects.filter(user=user)
        elif start_date:
            sales = Sale.objects.filter(created_at__gte=start_date)
        elif end_date:
            sales = Sale.objects.filter(created_at__lte=end_date)
        else:
            sales = sales
        return render(request, 'POS/sales_report.html',
                      context={'sales': sales, 'filter_form': SaleReportFilterForm(request.POST or None)})


class PaymentReportView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'POS/payment_report.html'
    context_object_name = 'payments'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter_form'] = PaymentReportFilterForm(self.request.POST)
        return context


class FilterPaymentsReportView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    model = Payment
    template_name = 'POS/payment_report.html'
    paginate_by = 5
    context_object_name = 'payments'

    def post(self, request):
        payment_reference = request.POST.get('payment_reference')
        sale_no = request.POST.get('sale_no')
        created_by_id = request.POST.get('created_by')
        paid_by = request.POST.get('paid_by')
        customer_id = request.POST.get('customer')
        payments = Payment.objects.all()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            payments = Payment.objects.filter(sale__customer_id=customer)
        elif created_by_id:
            user = User.objects.get(id=created_by_id)
            payments = Payment.objects.filter(sale__user=user)
        elif paid_by:
            payments = Payment.objects.filter(payment_by=paid_by)
        elif payment_reference:
            payments = Payment.objects.filter(payment_note=payment_reference)
        elif sale_no:
            payments = Payment.objects.filter(sale_id=sale_no)
        elif start_date:
            payments = Payment.objects.filter(created_at__gte=start_date)
        elif end_date:
            payments = Payment.objects.filter(created_at__lte=end_date)
        else:
            payments = payments
        return render(request, 'POS/payment_report.html',
                      context={'payments': payments, 'filter_form': PaymentReportFilterForm(request.POST or None)})


class RegisterReportView(LoginRequiredMixin, ListView):
    model = Register
    template_name = 'POS/registers_report.html'
    context_object_name = 'registers'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter_form'] = RegistersReportFilterForm(self.request.POST)
        return context


class FilterRegistersReportView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    model = Register
    template_name = 'POS/registers_report.html'
    paginate_by = 5
    context_object_name = 'registers'

    def post(self, request):
        user_id = request.POST.get('user')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        registers = Register.objects.all()
        if user_id:
            user = User.objects.get(id=user_id)
            registers = Register.objects.filter(user=user)
        elif start_date:
            registers = Register.objects.filter(updated_on__gte=start_date)
        elif end_date:
            registers = Register.objects.filter(updated_on__lte=end_date)
        else:
            registers = registers
        return render(request, 'POS/registers_report.html',
                      context={'registers': registers, 'filter_form': RegistersReportFilterForm(request.POST or None)})


class TopProductsView(LoginRequiredMixin, TemplateView):
    template_name = 'POS/top_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_date = datetime.datetime.now()
        first_day_of_current_month = current_date.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        third_month_ago = last_day_of_previous_month - datetime.timedelta(days=1)
        second_month_ago = third_month_ago.replace(day=1)
        first_month_ago = second_month_ago - datetime.timedelta(days=1)
        twelfth_month_ago = first_day_of_current_month - datetime.timedelta(days=365)
        first_day_of_twelfth_month_ago = twelfth_month_ago.replace(day=1)
        year_12_months_ago = twelfth_month_ago.year
        month_12_months_ago = calendar.month_name[twelfth_month_ago.month]
        current_month_products = SaleItem.objects.filter(created_at__month=datetime.datetime.now().month).values(
            'product__name').annotate(quantity=Sum('quantity')).order_by('-quantity')
        last_month_products = SaleItem.objects.filter(created_at__gte=first_day_of_previous_month,
                                                      created_at__lte=last_day_of_previous_month).values(
            'product__name').annotate(quantity=Sum('quantity')).order_by('-quantity')
        previous_three_months_products = SaleItem.objects.filter(created_at__gte=first_month_ago,
                                                                 created_at__lte=last_day_of_previous_month).values(
            'product__name').annotate(quantity=Sum('quantity')).order_by('-quantity')
        last_twelve_months_products = SaleItem.objects.filter(created_at__gte=first_day_of_twelfth_month_ago,
                                                              created_at__lte=last_day_of_previous_month).values(
            'product__name').annotate(quantity=Sum('quantity')).order_by('-quantity')
        context['current_month_products'] = current_month_products
        context['last_month_products'] = last_month_products
        context['previous_three_months_products'] = previous_three_months_products
        context['last_twelve_months_products'] = last_twelve_months_products
        current_month = calendar.month_name[datetime.datetime.now().month]
        last_month = calendar.month_name[first_day_of_previous_month.month]
        last_three_month = calendar.month_name[first_month_ago.month]
        current_year = datetime.datetime.now().year
        context['current_month'] = current_month
        context['last_month'] = last_month
        context['last_three_month'] = last_three_month
        context['current_year'] = current_year
        context['year_12_months_ago'] = year_12_months_ago
        context['month_12_months_ago'] = month_12_months_ago

        return context


class TopProductsReportView(LoginRequiredMixin, ListView):
    model = SaleItem
    template_name = 'POS/top_products_report.html'
    context_object_name = 'sales'
    queryset = SaleItem.objects.filter(sale__status='P').values('product__code', 'product__name').annotate(
        sold=Sum('quantity'), tax=Sum('product__product_tax'), cost=Sum('product__cost') * Sum('quantity'),
        income=Sum('price') * Sum('quantity'),
        profit=(Sum('price') * Sum('quantity')) - (Sum('product__cost')) * Sum('quantity'))
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter_form'] = ProductsReportFilterForm(self.request.POST)
        return context


class FilterProductsReportView(LoginRequiredMixin, MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    model = SaleItem
    template_name = 'POS/top_products_report.html'
    paginate_by = 5
    context_object_name = 'sales'

    def post(self, request):
        product_id = request.POST.get('products')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        sales = SaleItem.objects.filter(sale__status='P').values('product__code', 'product__name').annotate(
            sold=Sum('quantity'), tax=Sum('product__product_tax'), cost=Sum('product__cost') * Sum('quantity'),
            income=Sum('price') * Sum('quantity'),
            profit=(Sum('price') * Sum('quantity')) - (Sum('product__cost')) * Sum('quantity'))
        if product_id:
            product = Product.objects.get(id=product_id)
            sales = SaleItem.objects.filter(sale__status='P', product=product).values('product__code',
                                                                                      'product__name').annotate(
                sold=Sum('quantity'), tax=Sum('product__product_tax'), cost=Sum('product__cost') * Sum('quantity'),
                income=Sum('price') * Sum('quantity'),
                profit=(Sum('price') * Sum('quantity')) - (Sum('product__cost')) * Sum('quantity'))
        elif start_date:
            sales = SaleItem.objects.filter(sale__status='P', updated_at__gte=start_date).values('product__code',
                                                                                                 'product__name').annotate(
                sold=Sum('quantity'), tax=Sum('product__product_tax'), cost=Sum('product__cost') * Sum('quantity'),
                income=Sum('price') * Sum('quantity'),
                profit=(Sum('price') * Sum('quantity')) - (Sum('product__cost')) * Sum('quantity'))
        elif end_date:
            sales = SaleItem.objects.filter(sale__status='P', updated_at__lte=end_date).values('product__code',
                                                                                               'product__name').annotate(
                sold=Sum('quantity'), tax=Sum('product__product_tax'), cost=Sum('product__cost') * Sum('quantity'),
                income=Sum('price') * Sum('quantity'),
                profit=(Sum('price') * Sum('quantity')) - (Sum('product__cost')) * Sum('quantity'))
        else:
            sales = sales
        return render(request, 'POS/top_products_report.html',
                      context={'sales': sales, 'filter_form': ProductsReportFilterForm(request.POST or None)})
