from django.shortcuts import render
from .models import Title, Genre, Category
from django.db.models import Avg
from .serializers import TitleReadSerializer, TitleWriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets


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
