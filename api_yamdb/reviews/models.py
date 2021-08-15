from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Title(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.CharField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(
        'Genre', through='GenreTitle', related_name='genre'
    )
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='category'
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True,)
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self) -> str:
        return self.username
