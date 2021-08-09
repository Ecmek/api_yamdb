from django.urls import include, path
from rest_framework import routers, views
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1.urls)),
    path(
        'v1/auth/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
]
