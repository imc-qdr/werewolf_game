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

urlpatterns = [
    path('', views.index, name = 'index'),
    path('admin/', admin.site.urls, name = 'admin'),
    path('players/', views.getPlayers, name = 'getPlayers'),
    path('roles/', views.assignRoles, name = 'roles'),
    path('firstday', views.day1, name = 'day1'),
    path('seer', views.seer, name = 'seer'),
    path('seer1', views.seer1, name = 'seer1'),
    path('sleepwalk', views.sleepwalking, name = 'sleepwalking'),
    path('sleepwalk1', views.sleepwalking1, name = 'sleepwalking1'),
    path('sleepwalk2', views.sleepwalking2, name = 'sleepwalking2'),
    path('night', views.night, name = 'night_template'),
    path('witch', views.witch, name = 'witch'),
    path('white', views.whiteWerewolf, name = 'whiteWerewolf'),
    path('day', views.day, name = 'day_template'),
    path('humans_win', views.humans_win, name = 'humans_win'),
    path('werewolves_win', views.werewolves_win, name = 'werewolves_win'),
    path('hunter', views.hunter, name = 'hunter')
]
