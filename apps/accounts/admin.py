from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'banned', 'is_staff']
    list_filter = ['role', 'banned', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles & Status', {'fields': ('role', 'banned')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Roles & Status', {'fields': ('role', 'banned')}),
    )

admin.site.register(User, CustomUserAdmin)