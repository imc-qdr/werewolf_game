"""werewolf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('players/', views.getPlayers, name = 'getPlayers'),
    path('roles/', views.assignRoles, name = 'roles'),
    path('firstday', views.day1, name = 'day1'),
    path('night', views.night, name = 'night_template'),
    path('day', views.day, name = 'day_template')
]

urlpatterns += staticfiles_urlpatterns()

