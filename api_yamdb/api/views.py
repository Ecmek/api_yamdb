from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import (
    AdminUserSerializer, TokenSerializer, SignupSerializer
)
from .mails import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    @action(detail=False, url_path='me')
    def about_me(self, request):
        serializer = AdminUserSerializer(request.user)
        return Response(serializer.data)


class SignupAPIView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):

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
