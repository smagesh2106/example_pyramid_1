from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
# from .views import book, MyTokenObtainPairView
from .views import MyTokenObtainPairView, RegisterView2, ChangePasswordView, UserListView, update_user, \
    get_user, delete_user #, get_users UserDetailView,UserDeleteView,

# Register

urlpatterns = [
    # Registration, login, logout, password changes
    path('token/register', RegisterView2.as_view(), name="register_user"),
    path('token/login', MyTokenObtainPairView.as_view(), name='jwt_login'),
    path('token/logout', TokenBlacklistView.as_view(), name='jwt_logout'),
    path('token/changepassword', ChangePasswordView.as_view(), name='change-password'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    # User List, detailed view, update, delete
    path('users', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>', get_user, name='user-detail'),
    path('user/update/<int:pk>', update_user, name='user-update'),
    path('user/delete/<int:pk>', delete_user, name='user-delete'),

    # email password reset
    path('user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # Old
    # path('user/delete/<int:pk>', UserDeleteView.as_view(), name='user-delete')
    # path('user/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    # path('users', get_users, name='user-list'),

]

