from django.urls import path
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.index, name='index'),
    path('network/', views.network, name='network'),
    path('topology/', views.topology, name='topology'),
    path('analysis/', views.analysis, name='analysis'),
] 