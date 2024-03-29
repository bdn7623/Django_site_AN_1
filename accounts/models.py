import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone

from .managers import CustomUserManager
from .validators import validate_birth_date


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Attributes:
    - username (str): The username of the user.
    - email (str): The email address of the user.

    """

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class AbstractToken(models.Model):
    """
    Abstract model for token.

    Attributes:
    - user (CustomUser): The user associated with the token.
    - token (str): The token value.
    - created (datetime): The datetime when the token was created.

    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default='', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.token = get_random_string(32)
        super(AbstractToken, self).save(*args, **kwargs)

    def verify_token(self):
        validate_exp = timezone.localtime(self.created) > timezone.now() - timezone.timedelta(days=1)
        return validate_exp


class ActivationToken(AbstractToken):
    """
    Model for activation token.

    Attributes:
    - user (CustomUser): The user associated with the activation token.

    """

    def __str__(self):
        return f'{self.user.username}\'s activate token'

    class Meta:
        verbose_name_plural = 'Activation Tokens'


class PasswordResetToken(AbstractToken):
    """
    Model for password reset token.

    Attributes:
    - user (CustomUser): The user associated with the password reset token.

    """

    def __str__(self):
        return f'{self.user.username}\'s password reset token'

    class Meta:
        verbose_name_plural = 'Password Reset Tokens'


class Profile(models.Model):
    """
    Model for user profile.

    Attributes:
    - user (CustomUser): The user associated with the profile.
    - avatar (str): The URL of the user's avatar.
    - gender (str): The gender of the user.
    - date_of_birth (Date): The date of birth of the user.
    - bio (str): The biography of the user.
    - info (str): Additional information about the user.

    """

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='profile')
    avatar = models.URLField(max_length=255, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_birth_date])
    bio = models.TextField()
    info = models.CharField(max_length=250)

    def __str__(self):
        return f'Profile\'s of user {self.user.username}'

    def create_avatar(self):
        md5_hash = hashlib.md5(self.user.email.encode('utf-8')).hexdigest()
        gravatar_url = f'https://www.gravatar.com/avatar/{md5_hash}?d=identicon&s{200}'
        self.avatar = gravatar_url

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        if not self.avatar:
            self.create_avatar()
        super().save(*args, **kwargs)
