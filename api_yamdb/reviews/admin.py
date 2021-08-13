from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Comment, Review, Category, Genre, Title


admin.site.register(User, UserAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
