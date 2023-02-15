import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=16,
        choices=(
            ('user', 'Пользователь'),
            ('moderator', 'Модератор'),
            ('admin', 'Администратор'),
        ),
        default='user',
    )
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#uuidfield
    confirmation_code = models.UUIDField(
        'Код подтверждения',
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
