from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from .models import user

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

def register(request):
    if (request.POST):
        # Getting all data and save into a dictionary
        login_data = request.POST.dict()
        # Getting firstName
        firstname = login_data.get('firstName')
        lastName = login_data.get('lastName')
        address = login_data.get('address')
        email = login_data.get('email')
        dob = login_data.get('dob')
        gender = login_data.get('gender')
        username = login_data.get('username')
        password = login_data.get('password')
        digitpin = login_data.get('pwdCode')
        phone = login_data.get('phone')
        data = users(fname=firstname, lname=lastName, address=address, email=email, dob=dob, gender=gender, user_username=username, user_password=password, forget_pwd_code=digitpin, phone=phone, banned_status="N")
        data.save()
        return HttpResponseRedirect('registerSuccess')
    return render(request, 'ShoesInvasionApp/register.html')

def registerSuccess(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/register_success.html')