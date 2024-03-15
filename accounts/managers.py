from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.

    This manager provides methods for creating regular users and superusers.

    Attributes:
    - BaseUserManager: Django's base user manager class.
    """

    def create_user(self, email, username, first_name, last_name, password, **extra_fields):
        """
        Create a regular user.

        Parameters:
        - email (str): User's email address.
        - username (str): User's username.
        - first_name (str): User's first name.
        - last_name (str): User's last name.
        - password (str): User's password.
        - **extra_fields: Additional fields for the user model.

        Returns:
        - user: The created user object.

        Raises:
        - ValueError: If required fields are not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not first_name:
            raise ValueError('The First Name field must be set')
        if not last_name:
            raise ValueError('The Last Name field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **extra_fields):
        """
        Create a superuser.

        Parameters:
        - email (str): User's email address.
        - username (str): User's username.
        - first_name (str): User's first name.
        - last_name (str): User's last name.
        - password (str): User's password.
        - **extra_fields: Additional fields for the user model.

        Returns:
        - user: The created superuser object.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, first_name, last_name, password, **extra_fields)
