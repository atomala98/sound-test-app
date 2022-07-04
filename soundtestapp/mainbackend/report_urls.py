from django.urls import include, path

from . import report_views

urlpatterns = [
    path('<int:exam_no>', report_views.start, name='start')
]