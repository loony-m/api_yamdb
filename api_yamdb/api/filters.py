from django_filters import rest_framework

from reviews.models import Title


class GenreFilter(rest_framework.FilterSet):
    """Фильтр для класса Жанров."""
    genre = rest_framework.CharFilter(field_name='genre__slug')
    category = rest_framework.CharFilter(field_name='category__slug')
    year = rest_framework.NumberFilter(field_name='year')
    name = rest_framework.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        fields = ('genre', 'category', 'year', 'name')
        model = Title
