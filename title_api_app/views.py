from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from users_api_app.permissions import (IsAdminOrReadOnly,
                                       IsAuthorOrAdminOrModOrReadOnly)

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleSerializer)


class TitleViewSet(ModelViewSet):
    """
    CRUD для произведений.
    На чтение - любой пользователь, на запись - только администратор.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        """
        Из-за различного набора полей в json на чтение/запись используются
        разные сериализаторы.
        """
        if self.request.method in ['GET']:
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """
    CRUD для обзоров на произведения.
    На чтение - любой пользователь.
    На запись - только авторизованный с допограничениями
    в зависимости от операции.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)

    def get_queryset(self):
        title = generics.get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = generics.get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            title_id=title.pk,
        )


class CommentViewSet(ModelViewSet):
    """
    CRUD для комментариев к обзорам на произведения.
    На чтение - любой пользователь.
    На запись - только авторизованный с допограничениями
    в зависимости от операции.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModOrReadOnly,)

    def get_queryset(self):
        review = generics.get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title_id=self.kwargs['title_id'],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = generics.get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title_id=self.kwargs['title_id'],
        )
        serializer.save(
            author=self.request.user,
            review_id=review.pk,
        )


class CreateListDeleteModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    """
    Вьюсет, обеспечивающий просмотр всех записей, их добавление и удаление.
    """
    pass


class CategoryViewset(CreateListDeleteModelViewSet):
    """
    Просмотреть категории произведений (любой пользователь).
    Создать новую категорию (только администратор).
    Доступен поиск по названию категории.
    Удалить категорию произведения по слагу (только для администраторов).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ['=name', ]


class GenreViewset(CreateListDeleteModelViewSet):
    """
    Просмотреть жанры произведений (любой пользователь).
    Создать новый жанр (только администратор).
    Доступен поиск по названию жанра.
    Удалить жанр произведения по слагу (только для администраторов).
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ['=name', ]
