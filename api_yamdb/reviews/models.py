import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    # title = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)


################################################################################
################################################################################
class Title(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    # rating = models.IntegerField(null=True, blank=True)  # ??????????????????????????????????????????
    description = models.CharField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(
        'Genre', blank=True  # blank=True ???
    )
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True  # blank=True ???
    )


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
################################################################################


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True,)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(default=uuid.uuid4, max_length=36)
