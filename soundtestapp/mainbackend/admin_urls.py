from django.urls import path

from . import admin_views

urlpatterns = [
    path('', admin_views.login, name='login'),
]