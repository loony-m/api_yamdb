# API для Yatube

## Описание
Проект позволяет авторизованным пользователям ставить оценки разным произведениям, оставлять комментарии, отзывы к ним.

Работа над проектом в команде. Моя часть - views, serializers, команда для импорта данных из csv.

Стек: Django Rest Framework, djoser аутентификация по токену, redoc, pagination, permissions, throttling, django_filters.

## Как запустить проект:

1. Kлонируем репозиторий:
```
git clone 
```

2. Установим и активируем виртуальное окружение
```
python3 -m venv venv
```
```
. venv/bin/activate
```

3. Установим зависимости
```
pip install -r requirements.txt
```

4. Запустим проект
```
python manage.py runserver
```

## Документация к API:
Здесь описаны все доступные ендпоинты и примеры запросов к ним:
http://127.0.0.1:8000/redoc/

## Авторы
- [Александр Матияка](https://github.com/alexsevv)
- [Максим Краев](https://github.com/loony-m)
- [Алексей Алексеев](https://github.com/Litandepython)
