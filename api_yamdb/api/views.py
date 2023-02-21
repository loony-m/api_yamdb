
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, mixins, permissions, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (ReviewSerializer,
                             CommentSerializer,
                             CategoriesSerializer,
                             GenreSerializer,
                             TitleSerializerGet,
                             TitleSerializerPost,
                             UserMeSerializer,
                             UserSerializer,
                             UserSignUpSerializer,
                             UserTokenSerializer)
from api.permissions import (IsAdminOnlyPermission,
                             SelfEditUserOnlyPermission,
                             CheckAccessReview,
                             IsAdminOrReadOnly)
from reviews.models import (Title, Review, Categories,
                            Genre, Title)
from .mixins import CreateListDestroyViewSet
from users.models import User
from .filters import GenreFilter


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CheckAccessReview,)

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()

        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CheckAccessReview,)

    def get_review(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comment.all()

    def perform_create(self, serializer):
        review = self.get_review()

        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """
    Работает над всеми операциями с пользователями от лица админа.
    Позволяет обычному пользователю редактировать свой профиль.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOnlyPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(SelfEditUserOnlyPermission,)
    )
    def me_user(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        user = User.objects.get(username=request.user)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Регистрация пользователя с отправкой confirmation_code на электронную
    почту пользователя
    А также в случае, если пользователя зарегистрировал администратор.
    """
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if (User.objects.filter(username=request.data.get('username'),
                                email=request.data.get('email'))):
            user = User.objects.get(username=request.data.get('username'))
            serializer = UserSignUpSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get('username')
            user = get_object_or_404(User, username=username)
            code = user.confirmation_code
            send_mail(
                f'Код для получения токена для {user.username}',
                (f'Скопируйте этот confirmation_code: {code} '
                 f'для получения  токена по адресу api/v1/auth/token/'),
                'admin_yamdb@yandex.ru',
                [request.data.get('email')],
                fail_silently=False,
            )
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class TokenViewSet(viewsets.ViewSet):
    """
    Даем токен зарегистрированному пользователю
    """
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        context = 'Проверьте confirmation_code'
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=request.data.get('username')
            )
            if str(user.confirmation_code) == request.data.get(
                'confirmation_code'
            ):
                refresh = RefreshToken.for_user(user)
                token = {'token': str(refresh.access_token)}
                return Response(
                    token, status=status.HTTP_200_OK
                )
            return Response(
                context, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс представления произведений."""
    queryset = Title.objects.annotate(
        Avg('reviews__score')).order_by('name')
    pagination_class = PageNumberPagination
    serializer_class = TitleSerializerGet
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'year']
    http_method_names = ['get', 'post', 'delete', 'patch']
    filterset_class = GenreFilter
    permission_classes = [IsAdminOrReadOnly, ]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializerGet
        return TitleSerializerPost
