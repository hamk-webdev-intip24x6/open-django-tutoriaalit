from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import *

app_name = 'gallery'
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('image_upload', ImageUploadView.as_view(), name = 'image_upload'),
    path('success', TemplateView.as_view(template_name='gallery/success.html'), name = 'success'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
]