from django.urls import path

from . import admin_views

urlpatterns = [
    path('', admin_views.login, name='login'),
    path('admin_panel/', admin_views.admin_panel, name='admin_panel'),
    path('logout/', admin_views.logout, name='logout'),
    path('admin_panel/create_exam/', admin_views.create_exam, name='create_exam'),
    path('admin_panel/add_files/', admin_views.add_files, name='add_files'),
    path('admin_panel/exam_list/', admin_views.exam_list, name='exam_list'),
    path('admin_panel/exam_list/open_exam/<int:exam_id>', admin_views.open_exam, name='open_exam'),
    path('admin_panel/exam_list/close_exam/<int:exam_id>', admin_views.close_exam, name='close_exam'),
    path('admin_panel/add_one_file/<str:fileset_name>/<int:amount>', admin_views.add_one_file, name='add_one_file'),
    path('admin_panel/add_files_MUSHRA/<str:fileset_name>', admin_views.add_files_MUSHRA, name='add_files_MUSHRA'),
]