from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from blogs.models import Blog
from blogs.serializers import BlogSerializer


class BlogViewSet(ModelViewSet):
    """API Endpoint that retrieves the blog posts"""
    serializer_class = BlogSerializer
    queryset = Blog.objects.filter(active=True)
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['title', 'slug']
    filterset_fields = ['title', 'slug']
