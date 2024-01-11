from rest_framework import serializers
from django.urls import reverse

from cloths.models import Cloth, Comment
from accounts.models import Profile


class CommentSerializer(serializers.ModelSerializer):
    cloth = serializers.StringRelatedField(read_only=True)
    author = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Comment
        fields = "__all__"


class ClothSerializer(serializers.ModelSerializer):
    # relative_path = serializers.URLField(source='api_get_absolute_url',read_only=True)
    comments = serializers.SerializerMethodField(method_name="get_comments")
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Cloth
        fields = [
            "id",
            "title",
            "author",
            "description",
            "price",
            "active",
            "season",
            "gender",
            "absolute_url",
            "datetime_created",
            "datetime_modified",
            "comments",
        ]

        read_only_fields = ["author"]

    def get_comments(self, obj):
        comments = Comment.objects.filter(cloth=obj)[:3]
        return {
            "comments": CommentSerializer(comments, many=True).data,
        }

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = Profile.objects.get(user_id=request.user.id)
        return super().create(validated_data)

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context["kwargs"].get("pk"):
            rep.pop("absolute_url", None)
        return rep
