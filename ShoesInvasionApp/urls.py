from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ShoesInvasionApp'

urlpatterns = [
    # Home page Routing
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('home', views.index, name='index'),
    # About Page Routing
    path('about', views.about, name='about'),
    # Contact Page Routing
    path('home#contact', views.index, name='home'),
    # Shopping Cart Routing
    path('cart', views.cart, name='cart'),
     # Shop
    path('shop', views.shop, name='shop'),
     # Shoe Product
    path('shoeDetails', views.shoeDetails, name='shoeDetails'),
    # Login
    path('login/', views.login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # Register
    path('register', views.register, name='register'), 
    # Register Success
    path('registerSuccess/', views.registerSuccess, name='registerSuccess'),
    # Register Failed
    path('registerFailed/', views.registerFailed, name='registerFailed'),
]
