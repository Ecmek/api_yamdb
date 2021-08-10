from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import AdminUserSerializer, LoginSerializer, RegistrationSerializer
from .mails import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

    @action(detail=False, url_path='me')
    def about_me(self, request):
        serializer = AdminUserSerializer(request.user)
        return Response(serializer.data)


class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            try:
                user = User.objects.get(username=username, confirmation_code=confirmation_code)
            except User.DoesNotExist:
                return Response({'USER_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
            token = RefreshToken.for_user(user)
            return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
