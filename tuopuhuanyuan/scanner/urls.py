from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.submit_scan_task, name='submit_scan_task'),
    path('scan/<int:task_id>/', views.get_scan_status, name='get_scan_status'),
] 