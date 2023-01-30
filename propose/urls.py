from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from django.views.static import serve
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('verify', views.verify, name="verify"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('fillup', views.fillup, name="fillup"),
]
