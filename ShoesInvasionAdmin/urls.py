from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'ShoesInvasionAdmin'

urlpatterns = [
    # Home page Routing
    path('', views.login, name='index'),
    path('index', views.login, name='index'),
    path('login', views.login, name='index'),
    # User Table Route
    path('manage', views.manage, name='manage'),    
    path('ban_unban/', views.ban_unban, name='ban_unban'),
    path('logout/', views.logout, name='logout'),
    path('twoFA', views.twoFA, name='twoFA' ),
    path('createEditorAccount', views.createEditorAccount, name='createEditorAccount')
]

# For error 404 pages
handler404 = "ShoesInvasionApp.views.page_not_found_view"

# for error 500 pages
handler500 = "ShoesInvasionApp.views.server_error_view"

# for error 401 pages
handler401 = "ShoesInvasionApp.views.unauthorized_view"

# for error 502 pages
handler502 = "ShoesInvasionApp.views.bad_gateway_view"
