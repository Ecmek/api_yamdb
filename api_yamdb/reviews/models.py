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
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)


class Title(models.Model):
    None


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
