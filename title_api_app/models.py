from datetime import datetime as dt

from django.core import validators
from django.db import models

from users_api_app.models import CustomUser


class Category(models.Model):
    """
    Категории произведений (фильм, музыка и т.д.).
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название',
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанры произведений (драма, комедия и т.д.).
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название',
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Полная информация о произведениях.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='название'
    )
    description = models.TextField(
        blank=True,
        verbose_name='описание'
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        validators=[
            validators.MaxValueValidator(dt.today().year),
        ],
        verbose_name='год выпуска',
    )
    genre = models.ManyToManyField(
        to=Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанр',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='категория',
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.name} ({self.category})'


class Review(models.Model):
    """
    Обзоры на произведения.
    Не более одного обзора на одно и то же произведение от одного автора.
    """
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10),
        ],
        null=True,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата добавления комментария',
    )

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('author', 'text',)

    def __str__(self):
        return f'Ревью на {self.title} от {self.author}'


class Comment(models.Model):
    """
    Комментарии к обзорам на произведения.
    """
    author = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата добавления комментария',
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return (
            f'Коммент {self.author} к ревью {self.review.author}'
            f' на {self.review.title}'
        )
