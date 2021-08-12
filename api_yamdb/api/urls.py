from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, SignupAPIView, TokenAPIView, TitleViewSet, CategoryViewSet, GenreViewSet

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet)
v1.register('categories', CategoryViewSet)
v1.register('genres', GenreViewSet)
v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='login'),
    path('v1/auth/admin/', TokenObtainPairView.as_view())  # for admin token
]
