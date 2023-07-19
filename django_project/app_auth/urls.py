from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
# from .views import book, MyTokenObtainPairView
from .views import MyTokenObtainPairView, RegisterView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register_user"),
    path('login/', MyTokenObtainPairView.as_view(), name='jwt_login'),
    path('logout/', TokenBlacklistView.as_view(), name='jwt_logout'),
    path('changepassword/', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
