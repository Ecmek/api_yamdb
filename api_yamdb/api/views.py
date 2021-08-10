from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.models import User
from .serializers import (
    AdminUserSerializer, TokenSerializer, SignupSerializer, UserSerializer
)
from .permissions import IsRoleAdmin
from .mails import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False, url_path='me',
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        if request.method == 'GET':
            serializer = AdminUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(instance=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w\@\.\+\-\_]+)'
    )
    def get_user(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = AdminUserSerializer(user)
        if request.method == 'PACTH':
            serializer = AdminUserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        if request.method == 'DELETE':
            user.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(data=self.request.data, user=self.request.user)


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(User, username=username)

            try:
                user = User.objects.get(
                    username=username,
                    confirmation_code=confirmation_code
                )
            except User.DoesNotExist:
                return Response(
                    {"detail": "Not found."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
