from django.contrib import admin
from django.urls import path
from . import views

# Suggested code may be subject to a license. Learn more: ~LicenseLog:4033025260.
urlpatterns = [
    path('', views.index, name='home'),
]