from django.urls import path
from . import test_views

urlpatterns = [
    path('', test_views.index, name='index'),
    path('acr_test/', test_views.acr_test, name="Absolute Category Rating")
] 