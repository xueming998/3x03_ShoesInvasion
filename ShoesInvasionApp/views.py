from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from ShoesInvasionApp.models import products


from django.contrib import messages

from ShoesInvasionApp.forms import RegisterForm
from .models.user import UserTable
import bcrypt


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
    return render(request, 'ShoesInvasionApp/index.html#contact')

def cart(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/cart.html')

def shop(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    product = products.objects.all()
    return render(request, 'ShoesInvasionApp/shop.html',{'product':product})

def login(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/login_user.html')

def register(request):
    if request.method == 'POST':
        formDetails = RegisterForm(request.POST)
        if formDetails.is_valid():
            post = formDetails.save(commit = False)
            post.save()
            return render(request, 'ShoesInvasionApp/register_success.html')
        
        else:
            return render(request, 'ShoesInvasionApp/register.html', {'form': formDetails})
    
    else:
        form = RegisterForm(None)
        return render(request, 'ShoesInvasionApp/register.html', {'form':form})

    #     # Getting all data and save into a dictionary
    #     login_data = request.POST.dict()

    #     # Getting firstName
    #     firstname = login_data.get('firstName')
    #     lastName = login_data.get('lastName')
    #     address = login_data.get('address')
    #     email = login_data.get('email')
    #     dob = login_data.get('dob')
    #     gender = login_data.get('gender')
    #     username = login_data.get('username')
    #     password = login_data.get('password')
    #     verifyPassword = login_data.get('verify-password')
    #     phone = login_data.get('phone')
        

    #     if UserTable.objects.filter(username=username).exists():
    #         return render(request, 'ShoesInvasionApp/register_fail.html')
    #     else:
    #         # Need check what encryption level is this
    #         salt = bcrypt.gensalt()
    #         ecryptedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
    #         data = UserTable(
    #             fname=firstname, 
    #             lname=lastName, 
    #             address=address, 
    #             email=email, 
    #             dob=dob, 
    #             gender=gender, 
    #             username=username, 
    #             password=ecryptedPassword, 
    #             phone=phone, 
    #             bannedStatus=False,
    #             verifiedStatus=False,
    #             verificationCode=None,
    #             lockedStatus=False,
    #             lockedCounter=None,
    #             accountType="User"
    #             )
    #         data.save()
    #         return HttpResponseRedirect('registerSuccess')
    # return render(request, 'ShoesInvasionApp/register.html')

def registerSuccess(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/register_success.html')

def registerFailed(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/register_fail.html')