from django.urls import path
from user_accounts import views

urlpatterns = [
    path('add_user', views.CreateUserView.as_view(), name='add-user'),
    path('list_users', views.ListUserView.as_view(), name='list-users'),
]