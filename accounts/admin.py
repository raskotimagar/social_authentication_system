from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Contact Info', {'fields': ('email', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

