from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

from django.conf.urls import url


urlpatterns = [
	path('', include('django.contrib.auth.urls')),
	path('', views.dashboard, name='dashboard'),
	path('register/', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
    #path('activate/<str:uid>/<str:token>', views.activate_account, name='activate'),
    path('edit/', views.edit, name='edit'),
]

