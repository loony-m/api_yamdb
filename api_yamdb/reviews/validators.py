from rest_framework import serializers
from datetime import date


def check_year(value):
    if value < 0 or value > date.today().year:
        raise serializers.ValidationError('Некорректно указан год')
