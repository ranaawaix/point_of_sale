from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render, redirect

from POS.models import Register


class AdminRequiredMixin(AccessMixin):
    """Mixin that allows access only to admin users."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.group == 'A':
            return render(request, 'page_403.html')

        return super().dispatch(request, *args, **kwargs)


class StaffAdminRequiredMixin(AccessMixin):
    """Mixin that allows access only to staff or admin users."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not (request.user.group == 'S' or request.user.group == 'A'):
            return render(request, 'page_403.html')

        return super().dispatch(request, *args, **kwargs)


class StoreRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        reg = Register.objects.filter(user=request.user, status='O').first()
        if not reg:
            messages.error(request, 'Please select store and open the register first...')
            return redirect('stores')

        return super().dispatch(request, *args, **kwargs)
