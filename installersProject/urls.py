"""
URL configuration for installersProject project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from frontend.FrontendViews.usersFrontendView import *

admin.site.site_header = 'Shouka Django administration'
admin.site.site_title = 'Shouka Django administration site'
admin.site.index_title = 'Shouka Django Site Administration'

urlpatterns = [
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('apiv2/', include('apiv2.urls')),
    path('', include('frontend.urls')),
    path('main/', include('main.urls')),
    path('', include('pwa.urls')),
    # path('teska-main/', include('teska_main.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
