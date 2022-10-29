from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ShoesInvasionAdmin'

urlpatterns = [
    # Home page Routing
    path('', views.login, name='index'),
    # path('index', views.login, name='index'),
    # path('home', views.login, name='home'),
    path('login', views.login, name='login'),

    # User Table Route
    path('manage', views.manage, name='manage'),

    # Login API Point
    path('admin_login/', views.admin_login, name='admin_login'),
    
    path('ban_unban/', views.ban_unban, name='ban_unban'),
    path('logout/', views.logout, name='logout'),
]