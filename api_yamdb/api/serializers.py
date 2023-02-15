from reviews.models import Genre, Categories, Title
from rest_framework import serializers
from reviews.validators import check_year


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категорий"""
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerGet(serializers.ModelSerializer):
    """Сериализатор Title Get-запросов"""
    genre = GenreSerializer(many=True)
    category = CategoriesSerializer()
    year = serializers.IntegerField(validators=[check_year])
    # тут нужно будет еще рейтинг написать, пока не придумал

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerPost(serializers.ModelSerializer):
    """Сериализатор Title Post-запросов"""
    """Еще бы понять, как это писать..."""
    pass
