"""
URL configuration for plantilla project.

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
from . import settings
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('',views.home_view,name="home"),
    path('afterlogin',views.afterLogin,name="after"),
    path('dashboard/',views.dashboard_view,name="dashboard"),
    path('create/',include('generadorExamenes.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),

    # prueba correo
    path('prueba-correo/', views.prueba_envio_correo, name='prueba-correo'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,  document_root = settings.STATIC_ROOT)
