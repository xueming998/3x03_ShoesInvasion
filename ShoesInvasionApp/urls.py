from django.urls import path

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
    path('contact', views.contact, name='contact'),
    # Shopping Cart Routing
    path('cart', views.cart, name='cart'),
     # Shop
    path('shop', views.shop, name='shop'),
    # Login
    path('login', views.login, name='login'),
]