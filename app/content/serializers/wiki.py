from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ..models import WikiPost




class WikiPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikiPost
        fields = ["title", "content", "parent", "image","image_alt"]

class WikiPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikiPost
        fields = ["slug", "title", "content", "image","image_alt"]


class WikiFolderSerializer(serializers.ModelSerializer):
    children = SerializerMethodField()
    class Meta:
        model = WikiPost
        fields = ["slug", "title", "content", "children", "image","image_alt"]

    def get_children(self, obj):
        return [
            {
                "title":post.title,
                "slug":post.slug
            }
            for post in obj.get_children()
        ]