"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views.
For more information see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Django Admin
    path('admin/', admin.site.urls),
    

    # Authentication APIs
    path('api/auth/', include('accounts.urls')),

    # Product APIs
    path('api/products/', include('products.urls')),

    # Order APIs
    path('api/orders/', include('orders.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )