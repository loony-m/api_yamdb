from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


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
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """ Отзывы """
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                name='unique_author_title',
                fields=['author', 'title']
            )
        ]
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """ Комментарии к отзывам """
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comment'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
