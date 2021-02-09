from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from portfolio.api_views import (
    AboutViewSet, ProjectViewSet, SkillViewSet, JobExperienceViewSet, TestimonialViewSet
)
from blogs.api_views import BlogViewSet

from portfolio.views import TestimonialUpdateView, ThankYouView, HomeListView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeListView.as_view(), name='homepage'),

    path('client-comment-form/<slug:hash_key>/', TestimonialUpdateView.as_view(), name='client_comment_form'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),

    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# V1 API url patterns. Don't really need the namespacing feature since there aren't many views needed
router = routers.DefaultRouter()
router.register(r'about', AboutViewSet, basename='api-about')
router.register(r'project', ProjectViewSet, basename='api-project')
router.register(r'skill', SkillViewSet, basename='api-skill')
router.register(r'job-experience', JobExperienceViewSet, basename='api-job-experience')
router.register(r'testimonial', TestimonialViewSet, basename='api-testimonial')
router.register(r'blogs', BlogViewSet, basename='api-blog')

urlpatterns += [
    path('api/v1/', include(router.urls))
]
