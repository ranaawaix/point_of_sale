from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from user_accounts.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from user_accounts.forms import CreateUserForm, LoginForm, UserUpdateForm, AvatarForm, ChangePasswordForm

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

    def get_context_data(self, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        context = super().get_context_data(**kwargs)
        context['avatar_form'] = AvatarForm(self.request.POST)
        context['change_password_form'] = ChangePasswordForm(self.request.POST)
        context['user'] = user
        return context


class UpdateAvatarView(UpdateView):
    model = User
    form_class = AvatarForm
    template_name = 'user_accounts/update_user.html'
    success_url = 'list-users'

    def post(self, request, *args, **kwargs):
        avatar = request.FILES.get('avatar')
        user_id = kwargs['pk']
        user = User.objects.get(id=user_id)
        user.avatar = avatar
        user.save()
        return redirect(self.success_url)


class DeleteUserView(DeleteView):
    model = User
    template_name = 'user_accounts/confirm_delete.html'
    success_url = reverse_lazy('list-users')
