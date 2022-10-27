from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ShoesInvasionAdmin'

urlpatterns = [
    # Home page Routing
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('home', views.index, name='index'),
    path('login', views.login, name='login'),
    # adminLogin
    path('admin_login/', views.admin_login, name='admin_login'),
    
]