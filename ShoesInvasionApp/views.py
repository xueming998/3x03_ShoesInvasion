from asyncio.windows_events import NULL
# from math import prod
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from ShoesInvasionApp.models import productQuantity

# from .models.products import ProductsTable
# from ShoesInvasionApp.models import ProductsTable

from .models.products import ProductsTable
from .models.productQuantity import ProductQuantityTable

from django.contrib import messages

from ShoesInvasionApp.forms import RegisterForm
from .models.user import UserTable
import bcrypt

# Import for login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


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

def shoeDetails(request):
    shoeId = request.GET.get('id', '1')
    productQuery = ProductsTable.objects.filter(id = shoeId)
    productSize = ProductQuantityTable.objects.filter(product = shoeId)
    # Looping for product 
    for e in productQuery:
        # Looping for Quantity
        rangeLoop = 5 - int(e.review)
        product_size = []
        product_quantity = []
        product_color = []
        for a in productSize:
            if (a.color not in product_color):
                product_color.append(a.color)
            if (a.quantity not in product_quantity):
                product_quantity.append(a.quantity)
            if (a.size not in product_size):
                product_size.append(a.size)

        context = {
            'shoeId':shoeId,
            'product_name':e.product_name,
            'product_brand':e.product_brand,
            'product_category':e.product_category,
            'product_info':e.product_info,
            'product_price':e.product_price,
            'product_review':e.review, 
            'range':range(0,rangeLoop),
            'reviewLoop':range(0,int(e.review)),
            'product':productQuery, 
            'product_size':product_size,
            'product_quantity':product_quantity, 
            'product_color':product_color,
        }
    return render(request, 'ShoesInvasionApp/details.html',context)

def shop(request):
    shoeType = request.GET.get('type', "All Products")
    brand = request.GET.get('brand', "Any")
    gender = request.GET.get('gender', "Any")
    # product = ProductsTable.objects.all
    # No Filter 
    if (shoeType == "All Products" and brand == "Any" and gender == "Any"):
        product = ProductsTable.objects.all
    
    # Filter 
    elif (shoeType == "All Products" and brand != "Any" and gender != "Any" ):
        product = ProductsTable.objects.filter(product_brand = brand, gender_type = gender)
    elif (shoeType == "All Products" and brand == "Any" and gender != "Any" ):
        product = ProductsTable.objects.filter(gender_type = gender)
    elif (shoeType == "All Products" and brand != "Any" and gender == "Any" ):
        product = ProductsTable.objects.filter(product_brand = brand)

    elif (shoeType != "All Products" and brand == "Any" and gender == "Any" ):
        product = ProductsTable.objects.filter(product_category = shoeType)
    elif (shoeType != "All Products" and brand != "Any" and gender == "Any"):
        is_exist = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand).exists()
        if (is_exist == False):
            product = None
        else:
            product = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand)

    elif (shoeType != "All Products" and brand != "Any" and gender != "Any"):
        product = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, gender_type = gender)
    elif (shoeType != "All Products" and brand == "Any" and gender != "Any"):
        product = ProductsTable.objects.filter(product_category = shoeType,gender_type = gender)
    else:
        product = None

    context = {
        'product':product,
        'type':shoeType,
        'gender':brand,
        'brand' : gender, 
    }
    return render(request, 'ShoesInvasionApp/shop.html',context)

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            account = UserTable.objects.get(username=username)
            if checkPassword(password, account.password):
                return render(request, 'ShoesInvasionApp/register_success.html')
            else:
                return render(request, 'ShoesInvasionApp/register_fail.html')

        except UserTable.DoesNotExist:
            return render(request, 'ShoesInvasionApp/index.html')
    else:       
        form = AuthenticationForm()
        return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form})

def checkPassword(password, hashedPassword):
    if bcrypt.checkpw(password.encode('utf-8'), bytes(hashedPassword, 'utf-8')):
        return True
    else:
        return False

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