from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.models import Comment, Review, Title, User
from .mails import send_confirmation_code
from .permissions import IsRoleAdmin
from .serializers import (
    AdminUserSerializer,
    CommentSerializer,
    ReviewSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsRoleAdmin,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = (IsRoleAdmin,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


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
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
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
            serializer = UserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        if request.method == 'DELETE':
            user.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
