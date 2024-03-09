from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ActivationToken


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')


@admin.register(ActivationToken)
class ActivationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created')
    search_fields = ('user', 'token')
