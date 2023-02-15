from django.db import models
from django.db.models import UniqueConstraint


class Review(models.Model):
    """ Отзывы """
    # todo: изменить на ForeignKey и добавить on_delete
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.IntegerField(
        verbose_name='Автор'
    )
    title = models.IntegerField(
        verbose_name='Произведение'
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

    def __str__(self):
        return self.text


class Comment(models.Model):
    """ Комментарии к отзывам """
    # todo: изменить на ForeignKey и добавить on_delete
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.IntegerField(
        verbose_name='Автор'
    )
    review = models.IntegerField(
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.text


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
