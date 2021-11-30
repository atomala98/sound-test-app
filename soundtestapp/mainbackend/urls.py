from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('end_exam/', views.end_exam, name='end_exam'),
    path('interrupt/', views.interrupt, name='interrupt'),
    path('exam_handle/<str:exam_id>/<int:test_no>', views.exam_handle, name='exam_handle'),
    path('make_test/<str:exam_id>/<str:test_id>/<str:test_type_id>/<int:test_no>', views.make_test, name='make_test'),
] 