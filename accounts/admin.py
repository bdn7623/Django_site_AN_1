from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ActivationToken, PasswordResetToken, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.

    This class provides the admin interface configuration for CustomUser model.

    Attributes:
    - list_display (tuple): Fields to display in the list view.
    """

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')


@admin.register(ActivationToken)
class ActivationTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for ActivationToken model.

    This class provides the admin interface configuration for ActivationToken model.

    Attributes:
    - list_display (tuple): Fields to display in the list view.
    - search_fields (tuple): Fields to search in the admin interface.
    """

    list_display = ('user', 'token', 'created')
    search_fields = ('user', 'token')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for PasswordResetToken model.

    This class provides the admin interface configuration for PasswordResetToken model.

    Attributes:
    - list_display (tuple): Fields to display in the list view.
    - search_fields (tuple): Fields to search in the admin interface.
    """

    list_display = ('user', 'token', 'created')
    search_fields = ('user', 'token')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for Profile model.

    This class provides the admin interface configuration for Profile model.

    Attributes:
    - list_display (tuple): Fields to display in the list view.
    - list_filter (tuple): Fields for filtering in the admin interface.
    - search_fields (tuple): Fields to search in the admin interface.
    """

    list_display = ('user', 'gender', 'date_of_birth', 'info')
    list_filter = ('user', 'gender', 'date_of_birth')
    search_fields = ('user',)
