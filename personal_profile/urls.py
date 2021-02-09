from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from portfolio.views import TestimonialUpdateView, ThankYouView, HomeListView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeListView.as_view(), name='homepage'),

    path('client-comment-form/<slug:hash_key>/', TestimonialUpdateView.as_view(), name='client_comment_form'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),

    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('api/portfolio/', include('portfolio.api_urls', namespace='api-portfolio')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
