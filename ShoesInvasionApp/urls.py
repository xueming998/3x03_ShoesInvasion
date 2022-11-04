from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import re_path
from . import views

app_name = 'ShoesInvasionApp'

urlpatterns = [
    # Home page Routing
    path('', views.index, name=''),
    path('index', views.index, name='index'),
    path('home', views.index, name='home'),
    # About Page Routing
    path('about', views.about, name='about'),
    # Shopping Cart Routing
    path('cart', views.cart, name='cart'),
     # Shop
    path('shop', views.shop, name='shop'),
     # Shoe Product
    path('shoeDetails', views.shoeDetails, name='shoeDetails'),
    # Login
    path('login', views.login_request, name='login'),
    # Register
    path('register/', views.register_request, name='register'), 
    # Register Success
    path('registerSuccess/', views.registerSuccess, name='registerSuccess'),
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
    # email_verification_activate
    path('activate/<verificationcode>/<token>', views.activate, name='activate'),
     # PreOrder
    path('preOrder', views.preOrder, name='preOrder'),
    # Logout
    path('logout', views.logout, name='logout'),
    # 2FA
    # path('user_2fa/', views.user_2fa, name='user_2fa'),
]

# For error 404 pages
handler404 = "ShoesInvasionApp.views.page_not_found_view"

# for error 500 pages
handler500 = "ShoesInvasionApp.views.server_error_view"

# for error 401 pages
handler401 = "ShoesInvasionApp.views.unauthorized_view"

# for error 501 pages
handler501 = "ShoesInvasionApp.views.bad_gateway_view"
