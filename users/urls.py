from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Custom view instead of LoginView - the login form submits via
    # fetch() and expects a JSON response, not an HTML redirect
    # (see login_view in views.py and register.js on the frontend).
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.PlayerUpdateView.as_view(), name='player_update'),
    path('archive/', views.archive, name='archive'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html',
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete'),
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',
    ), name='password_reset_complete'),

    # DRF endpoints
    path('api/users/', views.UserListAPI.as_view(), name='user_api_list'),
    path('api/users/<int:pk>/', views.UserDetailAPI.as_view(), name='user_api_detail'),
    path('api/profiles/<int:pk>/', views.ProfileDetailAPI.as_view(), name='profile_api_detail'),
]