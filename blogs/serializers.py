from rest_framework import serializers

from blogs.models import Blog


class BlogSerializer(serializers.Serializer):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'cover', 'content', 'tags']