from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from django.views.static import serve
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('verify', views.verify, name="verify"),
    path('login', views.login, name="login"),
    path('home', views.home, name="home"),
]
