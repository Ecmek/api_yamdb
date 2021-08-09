from rest_framework import viewsets

from rewiews.models import Comment, Rewiew
from .serializers import CommentSerializer, RewiewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RewiewViewSet(viewsets.ModelViewSet):
    queryset = Rewiew.objects.all()
    serializer_class = RewiewSerializer
