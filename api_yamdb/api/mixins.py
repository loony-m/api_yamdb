from rest_framework import filters, viewsets
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   DestroyModelMixin)

from .permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(CreateModelMixin,
                               ListModelMixin,
                               DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы.
    Поддерживает обработку адреса с переменной slug.
    """
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('name',)
    lookup_field = 'slug'