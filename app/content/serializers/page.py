from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ..models import Page


class PageCreateSerializer(serializers.ModelSerializer):
    children = SerializerMethodField()
    path = SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            "slug",
            "title",
            "content",
            "parent",
            "children",
            "path",
            "image",
            "image_alt",
        ]

    def get_children(self, obj):
        return [{"title": post.title, "slug": post.slug} for post in obj.get_children()]

    def get_path(self, obj):
        return obj.get_path()

class PageSerializer(serializers.ModelSerializer):
    children = SerializerMethodField()
    path = SerializerMethodField()

    class Meta:
        model = Page
        fields = ["slug", "title", "content", "path", "children", "image", "image_alt"]

    def get_children(self, obj):
        return [{"title": post.title, "slug": post.slug} for post in obj.get_children()]

    def get_path(self, obj):
        return obj.get_path()


class PageTreeSerializer(serializers.ModelSerializer):
    children = SerializerMethodField()

    class Meta:
        model = Page
        fields = ["slug", "title", "children"]

    def get_children(self, obj):
        return [
            PageTreeSerializer(post).data
            for post in obj.get_children()]