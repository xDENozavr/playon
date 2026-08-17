from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/news', views.NewsViewSet, basename='news')

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
] + router.urls