from rest_framework import serializers

from .models import Ad, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["ad", "content"]


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["author", "ad", "content", "created_at", "updated_at"]

    def get_author(self, obj):
        return obj.author.name


class AdCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["title", "content"]


class AdListSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ["author", "title", "content", "created_at", "updated_at", "comments"]

    def get_author(self, obj):
        return obj.author.name
