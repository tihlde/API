from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ..models import Page




class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["title", "content", "parent", "image","image_alt"]

class PageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["slug", "title", "content", "image","image_alt"]


class PageSerializer(serializers.ModelSerializer):
    children = SerializerMethodField()
    class Meta:
        model = Page
        fields = ["slug", "title", "content", "children", "image","image_alt"]

    def get_children(self, obj):
        return [
            {
                "title":post.title,
                "slug":post.slug
            }
            for post in obj.get_children()
        ]