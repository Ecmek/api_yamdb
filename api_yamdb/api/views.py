from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='me')
    def about_me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
