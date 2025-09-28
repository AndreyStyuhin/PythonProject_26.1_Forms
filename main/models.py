from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # Заменяем username на email как основное поле для авторизации
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Дополнительные поля
    avatar = models.ImageField(
        _('avatar'),
        upload_to='users/avatars/',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        null=True
    )
    country = models.CharField(
        _('country'),
        max_length=100,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'  # Указываем поле для авторизации
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email