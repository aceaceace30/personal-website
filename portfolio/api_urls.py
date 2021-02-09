from . import api_views
from rest_framework import routers


app_name = 'portfolio'

router = routers.DefaultRouter()
router.register(r'about', api_views.AboutViewSet, basename='about')
router.register(r'project', api_views.ProjectViewSet, basename='project')
router.register(r'skill', api_views.SkillViewSet, basename='skill')
router.register(r'job-experience', api_views.JobExperienceViewSet, basename='job-experience')
router.register(r'testimonial', api_views.TestimonialViewSet, basename='testimonial')

urlpatterns = router.urls
