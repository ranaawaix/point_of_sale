from django.contrib import admin
from user_accounts.models import User, Groups
from django.contrib.auth.models import Group

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
