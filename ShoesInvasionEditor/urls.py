from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ShoesInvasionEditor'

urlpatterns = [
    # Home page Routing
    path('', views.login, name='login'),
    # path('index', views.login, name='index'),
    # path('home', views.login, name='home'),
    path('login', views.login, name='login'),
    # User Table Route
    path('manage', views.manage, name='manage'),
    # Login API Point
    path('admin_login/', views.admin_login, name='admin_login'),
    # path('createProduct/', views.createProduct, name='createProduct'),
    path('remove/', views.remove, name='remove'),
    path('create', views.create, name='create'), 
    path('logout/', views.logout, name='logout'),
    path('updateProduct/<str:pk>/', views.updateProduct, name='updateProduct'),
]