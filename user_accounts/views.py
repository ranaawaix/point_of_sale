from django.shortcuts import render
from user_accounts.models import User
from django.views.generic import CreateView, ListView
from user_accounts.forms import CreateUserForm

# Create your views here.


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'user_accounts/add_user.html'


class ListUserView(ListView):
    model = User
    queryset = User.objects.all()
    context_object_name = 'users'
    template_name = 'user_accounts/list_users.html'
