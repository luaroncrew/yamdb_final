from django.urls import include, path
from rest_framework.routers import DefaultRouter

from title_api_app.views import (
    CategoryViewset, CommentViewSet, GenreViewset, ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()

router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

router_v1.register(
    'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router_v1.register(
    'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments'
)

router_v1.register(
    'categories',
    CategoryViewset,
    basename='categories'
)

router_v1.register(
    'genres',
    GenreViewset,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
