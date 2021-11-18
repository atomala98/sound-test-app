from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('interrupt/', views.interrupt, name='interrupt'),
    path('exam_handle/<str:exam_id>/<int:test_no>', views.exam_handle, name='exam_handle'),
    path('make_test/<str:exam_id>/<str:test_id>/<str:test_type_id>/<int:test_no>', views.make_test, name='make_test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)