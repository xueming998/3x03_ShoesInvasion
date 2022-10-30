from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ShoesInvasionAdmin'

urlpatterns = [
    # Home page Routing
    path('', views.login, name='index'),
    path('index', views.login, name='index'),
    # User Table Route
    path('manage', views.manage, name='manage'),    
    path('ban_unban/', views.ban_unban, name='ban_unban'),
    path('logout/', views.logout, name='logout'),
    path('twoFA', views.twoFA, name='twoFA' )
]