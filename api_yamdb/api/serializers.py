from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from reviews.models import Review, Comment, Genre, Categories, Title
from reviews.validators import check_year
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if (value == 'me'):
            raise serializers.ValidationError(
                'Запрещено использовать me в качестве username'
            )
        return value


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if (value == 'me'):
            raise serializers.ValidationError(
                'Запрещено использовать me в качестве username'
            )
        return value


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator, ]
    )
    confirmation_code = serializers.CharField()
