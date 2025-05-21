from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    # API endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/profile/update/', views.update_profile_api, name='update_profile_api'),
    path('api/forgot-password/', views.forgot_password_api, name='forgot_password_api'),
] 