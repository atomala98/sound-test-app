from django.urls import path

from . import admin_views

urlpatterns = [
    path('', admin_views.login, name='login'),
    path('admin_panel/', admin_views.admin_panel, name='admin_panel'),
    path('logout/', admin_views.logout, name='logout'),
    path('admin_panel/create_exam/', admin_views.create_exam, name='create_exam'),
]