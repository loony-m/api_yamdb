from django.contrib.auth import get_user_model
from django.db import models
from .validators import check_year
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)

from django.db.models import UniqueConstraint

User = get_user_model()


class CategoriesAndGenreModel(models.Model):
    """Базовый класс для Категорий и Жанров"""
    name = models.CharField(max_length=256, verbose_name='имя')
    slug = models.SlugField(unique=True,max_length=50,
                            verbose_name='slug')

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Базовая модель'
        verbose_name_plural = 'Базовые модели'

    def __str__(self):
        return self.name


class Categories(CategoriesAndGenreModel):
    """Категории для произведений"""
    class Meta(CategoriesAndGenreModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoriesAndGenreModel):
    """Жанры для произведений"""
    class Meta(CategoriesAndGenreModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения"""
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


class GenreTitle(models.Model):
    """Класс, объединяющий Жанры и Произведения"""
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='ID жанра'
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения'
    )


class ReviewAndCommentModel(models.Model):
    """Базовый класс для Отзывов и Комментариев"""
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Review(ReviewAndCommentModel):
    """ Отзывы """
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10)),
        error_messages={'validators': 'Оценка должна быть от 1 до 10'},
        default=1,
        verbose_name='Оценка'
    )

    class Meta(ReviewAndCommentModel.Meta):
        constraints = [
            UniqueConstraint(
                name='unique_author_title',
                fields=['author', 'title']
            )
        ]
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewAndCommentModel):
    """ Комментарии к отзывам """
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comment'
    )

    class Meta(ReviewAndCommentModel.Meta):
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
