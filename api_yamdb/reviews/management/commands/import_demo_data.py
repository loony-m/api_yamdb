import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Genre, Categories, Title,
                            Review, Comment, GenreTitle)
from users.models import User


class Command(BaseCommand):
    help = "Команда для импорта жанров из csv"

    def data_user(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/users.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                User.objects.get_or_create(
                    pk=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3]
                )

    def data_genre(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/genre.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Genre.objects.get_or_create(
                    name=row[1],
                    slug=row[2]
                )

    def data_category(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/category.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Categories.objects.get_or_create(
                    name=row[1],
                    slug=row[2]
                )

    def data_title(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/titles.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Title.objects.get_or_create(
                    name=row[1],
                    year=row[2],
                    category=Categories.objects.get(id=row[3])
                )

    def data_genre_title(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/genre_title.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                GenreTitle.objects.get_or_create(
                    title_id=Title.objects.get(id=row[1]),
                    genre_id=Genre.objects.get(id=row[2])
                )

    def data_review(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/review.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Review.objects.get_or_create(
                    title=Title.objects.get(pk=row[1]),
                    text=row[2],
                    author=User.objects.get(pk=row[3]),
                    score=row[4],
                    pub_date=row[5]
                )

    def data_comments(self):
        path = os.path.join(
            settings.BASE_DIR, 'static/data/comments.csv'
        )

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Comment.objects.get_or_create(
                    review=Review.objects.get(pk=row[1]),
                    text=row[2],
                    author=User.objects.get(pk=row[3]),
                    pub_date=row[4]
                )

    def handle(self, *args, **kwargs):
        self.data_user()
        self.data_genre()
        self.data_category()
        self.data_title()
        self.data_genre_title()
        self.data_review()
        self.data_comments()
