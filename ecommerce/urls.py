"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path,include
from ecom_adminapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    
path('admin/', admin, name=' admin'),
path('admin/admin_login',admin_login, name='admin_login'),
path('', include('ecom_userapp.urls')),   # Include user app's URLs
path('', include('ecom_adminapp.urls')),  # Include admin app's URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)