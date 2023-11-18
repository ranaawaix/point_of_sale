from django.shortcuts import render
from django.urls import reverse_lazy
from user_accounts.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from user_accounts.forms import CreateUserForm, LoginForm, UserUpdateForm

# Create your views here.


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'user_accounts/add_user.html'
    success_url = reverse_lazy('list-users')


class ListUserView(ListView):
    model = User
    queryset = User.objects.all()
    context_object_name = 'users'
    template_name = 'user_accounts/list_users.html'


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user_accounts/login.html'


class UpdateUserView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_accounts/update_user.html'
    success_url = reverse_lazy('list-users')


class DeletUserView(DeleteView):
    model = User
    template_name = 'user_accounts/confirm_delete.html'
    success_url = reverse_lazy('list-users')
