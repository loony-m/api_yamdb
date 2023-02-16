from django.urls import path, include
from rest_framework import routers

from api.views import (ReviewViewSet,
                       CommentViewSet,
                       SignUpViewSet,
                       TokenViewSet,
                       UserViewSet)


router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

router.register('users', UserViewSet, basename='users')
router.register('auth/signup', SignUpViewSet, basename='sign-up')
router.register('auth/token', TokenViewSet, basename='token')

urlpatterns = [
    path('v1/', include(router.urls)),
]
