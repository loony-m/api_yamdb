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
