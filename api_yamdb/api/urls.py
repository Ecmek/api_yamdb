from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, RewiewViewSet

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/rewiews/(?P<rewiew_id>\d+)/comments',
    CommentViewSet
)
router.register(r'titles/(?P<title_id>\d+)/rewiews', RewiewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
