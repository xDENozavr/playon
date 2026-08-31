from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/clubs', views.ClubViewSet, basename='club')
router.register('api/team-categories', views.TeamCategoryViewSet, basename='team_category')
router.register('api/teams', views.TeamViewSet, basename='team')
router.register('api/games', views.GameViewSet, basename='game')

urlpatterns = [
    path('clubs/', views.club, name='club'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('calendar/', views.calendar, name='calendar'),
    path('teams/', views.teams, name='teams'),
    path('teams/create/', views.create_team, name='create_team'),
    path('rules/', views.rules, name='rules'),
    path('calendar/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
] + router.urls