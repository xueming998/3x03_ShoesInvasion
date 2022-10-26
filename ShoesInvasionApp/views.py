from asyncio.windows_events import NULL
from decimal import Decimal
import errno
from multiprocessing import context
from operator import truediv
from re import T
from telnetlib import STATUS
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from ShoesInvasionApp.models import productQuantity, shoppingCartTable
from ShoesInvasionApp.models import ShoppingCartTable
from .models.products import ProductsTable
from .models.productQuantity import ProductQuantityTable
from .models.transaction import TransactionTable
from .models.transactionDetails import TransactionDetailsTable
from datetime import datetime
import json
from django.http import JsonResponse
from django.contrib import messages

from ShoesInvasionApp.forms import RegisterForm
from ShoesInvasionApp.forms import UserLoginForm
from .models.user import UserTable
import bcrypt

from ShoesInvasionApp.models import user
from ShoesInvasionApp.models import transactionDetails
from ShoesInvasionApp.models import transaction

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


# Import for login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password


# Create your views here.
def index(request):
    unique_id = request.session['unique_id']
    print("unique_id", unique_id)
    return render(request, 'ShoesInvasionApp/index.html')

def about(request):
    return render(request, 'ShoesInvasionApp/about.html')

def contact(request):
    return render(request, 'ShoesInvasionApp/index.html#contact')

def cart(request):
    if request.session.has_key('unique_id'):
        print("Unique",request.session.get('unique_id'))
        cart = ShoppingCartTable.objects.filter(user='H6XZ2K2UpHfrRODM0ghtD0A7KkoXEd5aM8UGNWpBFZfBHtTRDBZkObabVYwWKptSDRKOHKzCRWhRJeqGA4hFftxoC0NK12bePgnPzvmI5VN34XAXZUjzX80ncst3sFybtxjuD0bNuxKECD0xf0Vb3PTZtFkCYE7pbJIIaY7dXm3h0hLfHbbAedq0L1CmatxduzSAydTi')
        total = 0
        for i in cart:
            total = i.getCartTotal


        context = {
            'cart':cart,
            'cartTotal':total,
            'user_id_string' : 'H6XZ2K2UpHfrRODM0ghtD0A7KkoXEd5aM8UGNWpBFZfBHtTRDBZkObabVYwWKptSDRKOHKzCRWhRJeqGA4hFftxoC0NK12bePgnPzvmI5VN34XAXZUjzX80ncst3sFybtxjuD0bNuxKECD0xf0Vb3PTZtFkCYE7pbJIIaY7dXm3h0hLfHbbAedq0L1CmatxduzSAydTi',
        }
        return render(request, 'ShoesInvasionApp/cart.html', context)
    else:
        return HttpResponseRedirect(request=request, template_name="ShoesInvasionApp/login_user.html")

# API CALL POINT 
def update_cartItem(request):
    data = json.loads(request.body)
    shoppingCartID = data['shoppingCartID']
    action = data['action']
    print(shoppingCartID)
    print(action)

    cartItem = ShoppingCartTable.objects.get(id = shoppingCartID)
    
    if action == "add":
        cartItem.quantity = (cartItem.quantity + 1)
        cartItem.total_price += cartItem.product.product_price 
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)
        cartItem.total_price -= cartItem.product.product_price 

    cartItem.save()

    if cartItem.quantity <= 0:
        cartItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def del_cartItem(request):
    data = json.loads(request.body)
    shoppingCartID = data['shoppingCartID']
    cartItem = ShoppingCartTable.objects.get(id = shoppingCartID)
    cartItem.delete()

    return JsonResponse('Item was deleted', safe=False)

def checkout_cartItem(request):
    data = json.loads(request.body)
    user_id = data['user_id']
    userObj = UserTable.objects.get(unique_id=user_id)

    t = TransactionTable.objects.create(user=userObj)
    t.save

    cartDetails = ShoppingCartTable.objects.filter(user = user_id)
    for i in cartDetails:
        shoe = ProductsTable.objects.get(id = i.product.id)
        tranDetails = TransactionDetailsTable.objects.create(transaction = t, product = shoe, quantity = i.quantity, size = i.size, amount = i.getCurrentProductTotal)
        tranDetails.save
        # Removing from shopping cart
        cartItemToDel = ShoppingCartTable.objects.get(id = i.id)
        cartItemToDel.delete()
        
    return JsonResponse('Shoes were sold', safe=False)

def add_to_cart(request):
    data = json.loads(request.body)
    # {'color':color,'size':size,'quantity':quantity,'shoe_id':productID,'user_id':1 }
    color = data['color']
    size = data['size']
    quantity = data['quantity']
    shoe_id = data['shoe_id']
    user_id = data['user_id']

    shoeObj = ProductsTable.objects.get(id=shoe_id)
    userObj = UserTable.objects.get(id=user_id)
    chosenTotalPrice = Decimal(shoeObj.product_price) * Decimal(quantity)
    t = ShoppingCartTable.objects.create(user = userObj, product = shoeObj, quantity = quantity, size = size, color = color, total_price = chosenTotalPrice)
    t.save

    # Insert Shoe here 
    return JsonResponse('Shoe Added', safe=False)

# Just to render Payment Success Page
def paymentSuccess(request):
    return render(request, 'ShoesInvasionApp/thankyou.html')

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
        # print(request.POST['data-sitekey'])
        try:
            account = UserTable.objects.get(username=username)

            if (account.accountType == 'User' and account.lockedStatus == 0):
                if checkPassword(password, account.password):
                    # Right Password | Change Locked Counter to 0
                    account.lockedCounter = 0
                    account.save()
                    return render(request, 'ShoesInvasionApp/register_success.html')
                else:
                    # Wrong Password | Need to append into Locked Counter
                    account.lockedCounter += 1
                    # Once Locked Counter = 3, Lock Account 
                    if (account.lockedCounter == 3):
                        account.lockedStatus = 1
                    account.save()
                    return render(request, 'ShoesInvasionApp/register_fail.html')

            else:
                # Wrong Account type. 
                return render(request, 'ShoesInvasionApp/register_fail.html')

        except UserTable.DoesNotExist:
            return render(request, 'ShoesInvasionApp/register_fail.html')
    else:       
        form = UserLoginForm()
        return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form})

def checkPassword(password, hashedPassword):
    if check_password(password, hashedPassword):
        print("True")
        return True
    else:
        print("False")
        return False

def register_request(request):
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

def registerSuccess(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/register_success.html')

def registerFailed(request):
    # template = loader.get_template("/index.html")
    # return HttpResponse(template.render())
    return render(request, 'ShoesInvasionApp/register_fail.html')