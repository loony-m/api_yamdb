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
        unique=True,
        max_length=254,
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

    @property
    def is_admin(self):
        return self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
