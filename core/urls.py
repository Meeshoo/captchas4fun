from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('play', views.play, name='/'),
    path('logout', views.logout, name='/'),
    path('leaderboard', views.leaderboard, name='/')
]