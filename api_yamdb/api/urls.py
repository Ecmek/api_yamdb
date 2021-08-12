from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CommentViewSet, ReviewViewSet, TitleViewSet
from .views import (
    CategoryViewSet, GenreViewSet, UserViewSet, SignupAPIView, TokenAPIView
)

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet)
v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)
v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
################################################################################
################################################################################
v1.register(r'titles', TitleViewSet)
v1.register(r'categories', CategoryViewSet)
v1.register(r'genres', GenreViewSet)
################################################################################

# v1.register(
#     r'comments',
#     CommentViewSet
# )
# v1.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='login'),
    path('v1/auth/admin/', TokenObtainPairView.as_view())  # for admin token
]
