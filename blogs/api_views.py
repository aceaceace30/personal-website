from rest_framework import viewsets

from blogs.filters import BlogFilter
from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """API Endpoint that retrieves the blog posts"""
    serializer_class = BlogSerializer
    queryset = Blog.objects.prefetch_related('tags')
    filter_class = BlogFilter

