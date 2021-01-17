from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from portfolio.models import About, Project, Skill, JobExperience, Testimonial
from portfolio.serializers import (
    AboutSerializer, ProjectSerializer, SkillSerializer, JobExperienceSerializer,
    TestimonialSerializer
)


class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    """API Endpoint that retrieves personal information used for Portfolio site"""
    serializer_class = AboutSerializer
    queryset = About.objects.order_by('pk')
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ['id', 'name', 'value']
    filterset_fields = ['name', 'value']
    search_fields = ['name', 'value']


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API Endpoint that retrieves the projects made"""
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('project_images')
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name', 'slug', 'classification']
    filterset_fields = ['name', 'slug', 'classification']


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """API Endpoint that retrieves the current skill set"""
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name', 'value', 'ordering', 'created_at']
    filterset_fields = ['active']


class JobExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    """API Endpoint that retrieves latest Job Experiences"""
    serializer_class = JobExperienceSerializer
    queryset = JobExperience.objects.prefetch_related('jobexperiencetask_set')
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['job_title', 'company', 'duration', 'created_at']
    filterset_fields = ['active']


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """API Endpoint that retrieves existing Testimonials"""
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['project_year', 'platform', 'created_at']
