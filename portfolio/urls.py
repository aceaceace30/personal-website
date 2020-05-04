from django.urls import path, include
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:name>/', views.detail, name='detail')
]
