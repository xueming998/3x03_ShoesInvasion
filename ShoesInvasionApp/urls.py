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
    path('login/', views.login_request, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # Register
    path('register', views.register_request, name='register'), 
    # Register Success
    path('registerSuccess', views.registerSuccess, name='registerSuccess'),
    # Register Failed 
    path('registerFailed', views.registerFailed, name='registerFailed'),
    # Thankyou.html (After Payment Successful )
    path('paymentSuccess', views.paymentSuccess, name='paymentSuccess'),
    # User Profile Page 
    path('profilePage', views.profilePage, name='profilePage'),
    path('viewUpdateProfilePage', views.viewUpdateProfilePage, name='viewUpdateProfilePage'),
    path('updateProfileDetails', views.updateProfileDetails, name='updateProfileDetails'),

    # Updating Cart Items from Fetch Call on Shopping Cart 
    path('update_cartItem/', views.update_cartItem, name='update_cartItem'),
    # Updating Cart Items from Fetch Call on Shopping Cart  
    path('del_cartItem/', views.del_cartItem, name='del_cartItem'),
    # Updating Cart Items from Fetch Call on Shopping Cart 
    path('checkout_cartItem/', views.checkout_cartItem, name='checkout_cartItem'),
    # add_to_cart
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
]
