from django.urls import path, reverse_lazy
from user_accounts import views
from user_accounts.forms import ChangePasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [path('add_user', views.CreateUserView.as_view(), name='add-user'),
               path('list_users', views.ListUserView.as_view(), name='list-users'),
               path('update_user/<int:pk>', views.UpdateUserView.as_view(), name='update-user'),
               path('update_avatar/<int:pk>', views.UpdateAvatarView.as_view(), name='update-avatar'),
               path('delete_user/<int:pk>', views.DeleteUserView.as_view(), name='delete-user'),
               path('change_password/<int:pk>',
                    auth_views.PasswordChangeView.as_view(form_class=ChangePasswordForm, template_name='user_accounts'
                                                                                                       '/update_user.html',
                                                          success_url=reverse_lazy('login')),
                    name='change-password'), path('login', views.UserLoginView.as_view(), name='login'),
               path('logout', views.LogoutView.as_view(), name='logout'), ]
