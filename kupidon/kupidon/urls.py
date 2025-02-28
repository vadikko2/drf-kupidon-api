"""
URL configuration for kupidon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from healthcheck import views as healthcheck_views
from images import views as images_views
from profiles import views as profiles_views
from .admins import admin

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Healthcheck
    path('', healthcheck_views.HealthCheckView.as_view(), name='healthcheck'),
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Profiles
    path('api/v1/profile/', profiles_views.ProfileView.as_view(), name='profile'),
    # Images
    path('api/v1/images/', images_views.ProfileImagesView.as_view(), name='images'),
]
