from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from portfolio.views import TestimonialUpdateView, ThankYouView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client-comment-form/<slug:hash_key>/', TestimonialUpdateView.as_view(), name='client_comment_form'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),
    path('', include('portfolio.urls', namespace='portfolio')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
