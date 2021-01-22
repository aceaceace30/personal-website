from django.urls import path
from . import views


app_name = 'blogs'


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list')
]
