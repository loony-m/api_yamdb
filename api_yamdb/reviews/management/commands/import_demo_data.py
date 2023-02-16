import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Genre, Categories, Title,
                            Review, Comment)
from users.models import User


class Command(BaseCommand):
    help = "Команда для импорта жанров из csv"

    def handle(self, *args, **kwargs):
        types = {
            User: os.path.join(
                settings.BASE_DIR, 'static/data/users.csv'
            ),
            Genre: os.path.join(
                settings.BASE_DIR, 'static/data/genre.csv'
            ),
            Categories: os.path.join(
                settings.BASE_DIR, 'static/data/category.csv'
            ),
            Title: os.path.join(
                settings.BASE_DIR, 'static/data/titles.csv'
            ),
            # todo: пока нет модели GenreTitle
            # GenreTitle: os.path.join(
            #     settings.BASE_DIR, 'static/data/genre_title.csv'
            # ),
            Review: os.path.join(
                settings.BASE_DIR, 'static/data/review.csv'
            ),
            Comment: os.path.join(
                settings.BASE_DIR, 'static/data/comments.csv'
            ),
        }

        for model, path in types.items():
            with open(path) as file:
                reader = csv.reader(file)
                next(reader)

                name = model.__name__

                if name == 'User':
                    for row in reader:
                        model.objects.get_or_create(
                            pk=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3]
                        )
                elif name == 'Genre' or name == 'Categories':
                    for row in reader:
                        model.objects.get_or_create(
                            name=row[1],
                            slug=row[2]
                        )
                elif name == 'Title':
                    for row in reader:
                        model.objects.get_or_create(
                            name=row[1],
                            year=row[2],
                            category=Categories.objects.get(id=row[3])
                        )
                elif name == 'GenreTitle':
                    for row in reader:
                        model.objects.get_or_create(
                            title_id=Title.objects.get(id=row[1]),
                            genre_id=Genre.objects.get(id=row[2])
                        )
                elif name == 'User':
                    for row in reader:
                        model.objects.get_or_create(
                            pk=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3]
                        )
                elif name == 'Review':
                    for row in reader:
                        model.objects.get_or_create(
                            title=Title.objects.get(pk=row[1]),
                            text=row[2],
                            author=User.objects.get(pk=row[3]),
                            score=row[4],
                            pub_date=row[5]
                        )
                elif name == 'Comment':
                    for row in reader:
                        model.objects.get_or_create(
                            review=Review.objects.get(pk=row[1]),
                            text=row[2],
                            author=User.objects.get(pk=row[3]),
                            pub_date=row[4]
                        )
