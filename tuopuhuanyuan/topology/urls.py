from django.urls import path
from . import views

app_name = 'topology'

urlpatterns = [
    # API endpoints
    path('api/topologies/', views.topology_list_api, name='topology_list_api'),
    path('api/topologies/create/', views.topology_create_api, name='topology_create_api'),
    path('api/topologies/<int:pk>/', views.topology_detail_api, name='topology_detail_api'),
    path('api/topologies/<int:pk>/update/', views.topology_update_api, name='topology_update_api'),
    path('api/topologies/<int:pk>/delete/', views.topology_delete_api, name='topology_delete_api'),
    path('api/topologies/<int:pk>/analyze/', views.topology_analyze_api, name='topology_analyze_api'),
] 