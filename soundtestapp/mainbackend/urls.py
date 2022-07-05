from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('end_exam/', views.end_exam, name='end_exam'),
    path('interrupt/', views.interrupt, name='interrupt'),
    path('exam_handle/', views.exam_handle, name='exam_handle'),
] 