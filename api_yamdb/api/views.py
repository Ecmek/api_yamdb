from reviews.models import Title, Genre, Category, Review, Comment
from django.db.models import Avg
from .serializers import (TitleReadSerializer,
                          TitleWriteSerializer,
                          CommentSerializer,
                          RewiewSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from api.filters import TitleFilter
from .permissions import IsRoleAdmin


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleReadSerializer
    queryset = Title.objects.annotate(rating=Avg(
        'reviews__score')).order_by('-id')
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAdminUser,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsRoleAdmin,)


class RewiewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = RewiewSerializer
    permission_classes = (IsRoleAdmin,)
