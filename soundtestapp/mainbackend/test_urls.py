from django.urls import path
from . import test_views

urlpatterns = [
    path('', test_views.index, name='index'),
    path('acr_test/', test_views.acr_test, name="Absolute Category Rating"),
    path('dcr_test/', test_views.dcr_test, name="Degradation Category Rating"),
    path('ccr_test/', test_views.ccr_test, name="Comparison Category Rating"),
    path('mushra/', test_views.mushra, name="MUSHRA"),
    path('abx_test/', test_views.abx_test, name="ABX Test"),
    path('abchr_test/', test_views.abchr_test, name="ABC/HR Test")
] 