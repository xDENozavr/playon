from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Custom view instead of LoginView — the login form submits via
    # fetch() and expects a JSON response, not an HTML redirect
    # (see login_view in views.py and register.js on the frontend).
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # DRF endpoints
    path('api/users/', views.UserListAPI.as_view(), name='user_api_list'),
    path('api/users/<int:pk>/', views.UserDetailAPI.as_view(), name='user_api_detail'),
    path('api/profiles/<int:pk>/', views.ProfileDetailAPI.as_view(), name='profile_api_detail'),
]