from django.urls import path

from . import views

app_name = 'ShoesInvasionApp'

urlpatterns = [
    path('', views.index, name='index'),
]