from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class ActivationToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default='', unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s activate token'

    class Meta:
        verbose_name_plural = 'Activation Tokens'

    def save(self, *args, **kwargs):
        self.token = get_random_string(32)
        super(ActivationToken, self).save(*args, **kwargs)

    def verify_token(self):
        validate_exp = timezone.localtime(self.created) > timezone.now() - timezone.timedelta(days=1)
        return validate_exp