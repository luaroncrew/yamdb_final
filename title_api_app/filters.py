from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтры по категории, жанру, названию и году выхода произведения.
    """
    category = filters.CharFilter(
        field_name='category__slug',
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year', ]
