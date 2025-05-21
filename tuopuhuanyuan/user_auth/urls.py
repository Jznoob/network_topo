from django.urls import path
from . import views
from .views import LogoutApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

app_name = 'user_auth'

urlpatterns = [
    # API endpoints
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', LogoutApiView.as_view(), name='logout_api'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/profile/update/', views.update_profile_api, name='update_profile_api'),
    path('api/forgot-password/', views.forgot_password_api, name='forgot_password_api'),
    path('api/reset-password/', views.reset_password_api, name='reset_password_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] 