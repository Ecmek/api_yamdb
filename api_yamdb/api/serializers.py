from rest_framework import serializers

from rewiews.models import Comment, Rewiew


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'rewiew', 'text', 'author', 'pub_date')
        model = Comment


class RewiewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Rewiew
