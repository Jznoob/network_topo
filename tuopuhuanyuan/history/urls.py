from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    # API endpoints
    path('api/histories/', views.history_list_api, name='history_list_api'),
    path('api/histories/<int:pk>/', views.history_detail_api, name='history_detail_api'),
    path('api/histories/<int:pk>/delete/', views.history_delete_api, name='history_delete_api'),
    path('api/histories/clear/', views.history_clear_api, name='history_clear_api'),
] 