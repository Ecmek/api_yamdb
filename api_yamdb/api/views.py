from rest_framework import viewsets

from rewiews.models import Comment, Rewiew
from .permissions import IsRoleAdmin
from .serializers import CommentSerializer, RewiewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsRoleAdmin,)


class RewiewViewSet(viewsets.ModelViewSet):
    queryset = Rewiew.objects.all()
    serializer_class = RewiewSerializer
    permission_classes = (IsRoleAdmin,)
