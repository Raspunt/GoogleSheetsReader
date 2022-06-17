from unicodedata import name
from django.contrib import admin
from django.urls import path, include

from . views import StartPage

urlpatterns = [
    path('',StartPage,name="StartPageUrl"),
]
