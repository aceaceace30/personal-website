from rest_framework.viewsets import ModelViewSet

from blogs.filters import BlogFilter
from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogViewSet(ModelViewSet):
    """API Endpoint that retrieves the blog posts"""
    serializer_class = BlogSerializer
    queryset = Blog.objects.prefetch_related('tags')
    filter_class = BlogFilter

