from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from portfolio.views import TestimonialUpdateView, ThankYouView
from portfolio import api_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'about', api_views.AboutViewSet, basename='about')
router.register(r'project', api_views.ProjectViewSet, basename='project')
router.register(r'skill', api_views.SkillViewSet, basename='skill')
router.register(r'job-experience', api_views.JobExperienceViewSet, basename='job-experience')
router.register(r'testimonial', api_views.TestimonialViewSet, basename='testimonial')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('client-comment-form/<slug:hash_key>/', TestimonialUpdateView.as_view(), name='client_comment_form'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),
    path('', include('portfolio.urls', namespace='portfolio')),
    path('blogs/', include('blogs.urls', namespace='blogs'))
]

urlpatterns += [
    path('api/v1/', include((router.urls, 'portfolio'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
