from django.urls import path
from user_accounts import views

urlpatterns = [
    path('add_user', views.CreateUserView.as_view(), name='add-user'),
    path('list_users', views.ListUserView.as_view(), name='list-users'),
    path('update_user/<int:pk>', views.UpdateUserView.as_view(), name='update-user'),
    path('delete_user/<int:pk>', views.DeletUserView.as_view(), name='delete-user'),
    path('login', views.UserLoginView.as_view(), name='login'),
]