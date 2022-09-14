from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/index.html')

def about(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/about.html')

def contact(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/contact.html')

def cart(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/cart.html')

def shop(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/shop.html')

def login(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/login_user.html')