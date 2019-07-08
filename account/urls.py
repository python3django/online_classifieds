from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('edit/', views.edit, name='edit'),
]

