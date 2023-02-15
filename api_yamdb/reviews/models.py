from django.db import models
from .validators import check_year


class Categories(models.Model):
    """Категории для произведений"""
    name = models.CharField(max_length=256, verbose_name='имя')
    slug = models.SlugField(unique=True, max_length=64,
                            verbose_name='slug')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Жанры для произведений"""
    name = models.CharField(max_length=256, verbose_name='имя')
    slug = models.SlugField(unique=True, max_length=64,
                            verbose_name='slug')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения"""
    """В ТЗ написано: При удалении объекта категории Category не нужно
     **удалять связанные с этой категорией произведения.(с)
     по идее я описал верно удаление, но проверьте."""
    name = models.CharField(max_length=256, verbose_name='имя')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Категория')
    year = models.IntegerField(verbose_name='Год',
                               validators=[check_year])
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name






