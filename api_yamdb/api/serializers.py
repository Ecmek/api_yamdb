from django.core.mail import send_mail
from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role', 'confirmation_code'
        )

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'])

        send_mail(
            'Сonfirmation code YaMDb.ru',
            f'Ваш код подтверждения: {user.confirmation_code}',
            'admin@YaMDb.ru',
            [user.email],
            fail_silently=False,
        )
        return user
