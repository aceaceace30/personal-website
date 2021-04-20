from rest_framework import serializers

from blogs.models import Blog, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'color']


class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'cover', 'content', 'tags']