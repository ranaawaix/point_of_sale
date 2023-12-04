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
    StoreProductForm, CashInHandForm
from POS.models import Sale, Hold, Customer, Payment, Register
from POS.models import Store, StoreProduct
from inventory.models import Product
from user_accounts.models import User


# Create your views here.


class StoreListView(ListView):
    model = Store
    queryset = Store.objects.all()
    template_name = 'POS/list_stores.html'
    context_object_name = 'stores'
    paginate_by = 5


class POS(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'POS/pos.html'
    success_url = reverse_lazy('stores')

    def get_context_data(self, *args, **kwargs):
        register_id = self.kwargs['register_id']
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
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


class SaleView(TemplateView):
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


class SaleItemUpdateView(TemplateView):
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


class HoldOrderView(CreateView):
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


class AddCustomerView(CreateView):
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


class PaymentView(CreateView):
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


class DeleteSaleItemView(TemplateView):
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


class AddStoreView(CreateView):
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


class AddCustomersView(CreateView):
    model = Customer
    form_class = AddCustomerForm
    template_name = 'POS/add_customer.html'
    success_url = reverse_lazy('list-customers')


class ListCustomersView(ListView):
    model = Customer
    template_name = 'POS/list_customers.html'
    context_object_name = 'customers'
    paginate_by = 5


class UpdateCustomerView(UpdateView):
    model = Customer
    form_class = AddCustomerForm
    template_name = 'POS/update_customer.html'
    success_url = reverse_lazy('list-customers')


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = 'POS/confirm_delete.html'
    success_url = reverse_lazy('list-customers')


class ProductListView(ListView):
    model = StoreProduct
    template_name = 'POS/list_products.html'
    context_object_name = 'storeproducts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['stores'] = Store.objects.all()
        return context


class StoreWiseProductListView(MultipleObjectTemplateResponseMixin, MultipleObjectMixin, View):
    model = StoreProduct
    template_name = 'POS/list_products.html'

    def get(self, request, pk):
        stores = Store.objects.all()
        store = Store.objects.get(id=pk)
        self.queryset = StoreProduct.objects.filter(store=store)
        return render(request, template_name=self.template_name,
                      context={'stores': stores, 'store': store, 'storeproducts': self.queryset})


class AddProductView(CreateView):
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


class UpdateProductView(UpdateView):
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


class DeleteProductView(DeleteView):
    model = Product
    template_name = 'POS/confirm_delete_product.html'
    success_url = reverse_lazy('list-products')


class SaleListView(ListView):
    model = Sale
    template_name = 'POS/list_sales.html'
    queryset = Sale.objects.filter(status='P')
    context_object_name = 'sales'
    paginate_by = 5


class OpenedBillsView(ListView):
    model = Sale
    template_name = 'POS/list_opened_bills.html'
    queryset = Sale.objects.filter(status='H')
    context_object_name = 'sales'
    paginate_by = 5


class POSUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'POS/pos.html'
    success_url = reverse_lazy('list-opened-bills')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(object=self.object)
        context['products'] = Product.objects.all()
        context['holdform'] = HoldOrderForm(self.request.POST or None, instance=self.object)
        context['customerform'] = AddCustomerForm(self.request.POST or None, instance=self.object)
        context['paymentform'] = PaymentForm(self.request.POST or None, instance=self.object)
        return context


class POSDeleteView(DeleteView):
    model = Sale
    template_name = 'POS/confirm_delete_sale.html'
    success_url = reverse_lazy('list-opened-bills')


class StoreSelectView(SingleObjectMixin, View):

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
                          context={'selected_store': selected_store, 'form': form})
        else:
            messages.error(self.request, 'You are not authorized to enter this store')
            return render(request, template_name='POS/list_stores.html', context={'stores': stores})


class CashInHandView(CreateView):
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
            return redirect('create-sale', register_id=register_id)
        else:
            messages.error(self.request,
                           'Please enter the opening cash in hand amount. Enter "0" if no opening amount.')
            return render(request, template_name='POS/register.html',
                          context={'selected_store': register, 'form': form})


class CloseRegisterView(View):

    def post(self, request):
        register_id = request.POST.get('register_id')
        register = Register.objects.get(id=register_id)
        register.closing_cash_in_hand = \
            register.saleitems.filter(register_id=register_id).aggregate(closing_cash_in_hand=Sum('total'))[
                'closing_cash_in_hand']
        register.status = 'C'
        register.save()
        return redirect('stores')
