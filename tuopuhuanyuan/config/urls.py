from django.urls import path
from . import views

app_name = 'config'

urlpatterns = [
    # API endpoints
    path('api/configs/', views.config_list_api, name='config_list_api'),
    path('api/configs/create/', views.config_create_api, name='config_create_api'),
    path('api/configs/<int:pk>/', views.config_detail_api, name='config_detail_api'),
    path('api/configs/<int:pk>/update/', views.config_update_api, name='config_update_api'),
    path('api/configs/<int:pk>/delete/', views.config_delete_api, name='config_delete_api'),
] 