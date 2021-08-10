from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, RegistrationAPIView, LoginAPIView

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view(), name='signup'),
    path('v1/auth/token/', LoginAPIView.as_view(), name='login'),
]
