import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


# class UserManager(BaseUserManager):
#     """Create and return a `User` with an email, username"""
#     def create_user(self, username, email, password=None, role='user',
#                     bio=None):
#         if username is None:
#             raise TypeError('Users must have a username.')

#         if email is None:
#             raise TypeError('Users must have an email address.')

#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()

#         return user

#     def create_superuser(self, username, email, password, role='admin',
#                          bio=None):
#         """
#         Create and return a `User` with superuser (admin) role.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

#         return user


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
