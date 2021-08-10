from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from rewiews.models import Comment, Rewiew, Title


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'rewiew', 'text', 'author', 'pub_date')
        model = Comment


class RewiewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Rewiew

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError(
                'Оценкой должно быть целое число от 1 до 10.'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'rating')

    def get_rating(self, obj):
        title = get_object_or_404(Title, id=obj.id)
        rating = title.rewiews.all().aggregate(Avg('score'))
        return rating
