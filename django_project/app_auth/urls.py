from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

# from .views import book, MyTokenObtainPairView
from .views import MyTokenObtainPairView, RegisterView2, ChangePasswordView, UserListView, update_user, UserDeleteView, \
    get_user, toggle_admin_previlege, AdminUsers

#delete_user, UserDetailedView #, get_users UserDetailView,UserDeleteView,

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
    path('user/admins', AdminUsers.as_view(), name='admin-list'),
    path('users', UserListView.as_view(), name='user-list'),
    path('user/delete/<int:pk>', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>', get_user, name='user-detail2'),
    path('user/update/<int:pk>', update_user, name='user-update'),
    path('user/manage_admin/<int:pk>', toggle_admin_previlege, name='user-upgrade'),

    # email password reset
    path('user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

