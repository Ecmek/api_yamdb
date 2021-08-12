from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, code, signup, token

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='login'),
    path('v1/auth/code/', code, name='code'),
]
