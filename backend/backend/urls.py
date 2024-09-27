"""
URL configuration for backend project.

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

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    """
    Home view that returns a welcome message.
    """
    return HttpResponse(
        "Welcome to the home page, run your frontend for the complete user experience! "
        "Thank you!"
    )

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home_view),
    path('accounts/', include('allauth.urls')),
    path('api/', include('api.urls')),
]