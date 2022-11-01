from asyncio.windows_events import NULL
from decimal import Decimal
from enum import unique
import errno
from itertools import product
from mimetypes import init
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
from ShoesInvasionApp.models.preorder import PreOrderTable
from .models.products import ProductsTable
from .models.productQuantity import ProductQuantityTable
from .models.transaction import TransactionTable
from .models.transactionDetails import TransactionDetailsTable
from .models.preorder import PreOrderTable
from datetime import datetime
import json
from django.http import JsonResponse
from django.contrib import messages

from ShoesInvasionApp.forms import RegisterForm
from ShoesInvasionApp.forms import UserLoginForm
from .models.user import UserTable 
from .models.userDetails import UserDetailsTable

from ShoesInvasionApp.models import user
from ShoesInvasionApp.models import transactionDetails
from ShoesInvasionApp.models import transaction

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


# Import for login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

# Import for 2FA
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO

#Import for Logging
import logging
logger=logging.getLogger('user')
#from ShoesInvasionApp import signals

# Create your views here.
def index(request):
        return render(request, 'ShoesInvasionApp/index.html')

def about(request):
    return render(request, 'ShoesInvasionApp/about.html')

def contact(request):
    return render(request, 'ShoesInvasionApp/index.html#contact')

def cart(request):
    try:
        if request.session.has_key('unique_id'):
            uid = request.session['unique_id']
            cart = ShoppingCartTable.objects.filter(user=uid)
            total = 0
            for i in cart:
                total = i.getCartTotal


            context = {
                'cart':cart,
                'cartTotal':total,
                'user_id_string' : uid,
            }
            return render(request, 'ShoesInvasionApp/cart.html', context)
        else:
            return HttpResponseRedirect(request=request, template_name="ShoesInvasionApp/login_user.html")
    except:
        return redirect('login/')

# API CALL POINT 
def update_cartItem(request):
    try:
        if request.session.has_key('unique_id'):
            # Ensure deleting only when logged in. 
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
        else:
            return redirect('login/')

    except:
        return redirect('login/')

def del_cartItem(request):
    try:
        # Ensure only deleting when logged in
        if request.session.has_key('unique_id'):
            data = json.loads(request.body)
            shoppingCartID = data['shoppingCartID']
            cartItem = ShoppingCartTable.objects.get(id = shoppingCartID)
            cartItem.delete()

            return JsonResponse('Item was deleted', safe=False)
        else:
            return redirect('login/')
    except:
        return redirect('login/')

def checkout_cartItem(request):
    try:
        if request.session.has_key('unique_id'):
            uid = request.session['unique_id']
            data = json.loads(request.body)
            user_id = data['user_id']
            userObj = UserTable.objects.get(unique_id=user_id)
            cartDetails = ShoppingCartTable.objects.filter(user = uid)
            t = TransactionTable.objects.create(user=userObj)
            t.save
            for i in cartDetails:
                shoe = ProductsTable.objects.get(id = i.product.id)
                tranDetails = TransactionDetailsTable.objects.create(transaction = t, product = shoe, quantity = i.quantity, size = i.size, amount = i.getCurrentProductTotal)
                tranDetails.save
                # Adding pre-order shoes into pre-order table
                if (i.status == "2"):
                    save = ""
                    save = PreOrderTable.objects.create(product = shoe, unique_id = userObj)
                    save.save()
                else:
                    pass
                # Removing from shopping cart
                cartItemToDel = ShoppingCartTable.objects.get(id = i.id)
                cartItemToDel.delete()
                
            return JsonResponse('Shoes were sold', safe=False)
        else:
            return redirect("login/")
    except:
        return redirect("login/")

def add_to_cart(request):
    try:
        if request.session.has_key('unique_id'):
            print("Unique",request.session.get('unique_id'))
            uid = request.session['unique_id']
            data = json.loads(request.body)
            print("Unique", data)
            # {'color': 'BLUE', 'size': 'UK 7', 'quantity': '1', 'shoe_id': '3', 'user_id': 1, 'status': '1'}
            color = data['color']
            size = data['size']
            quantity = data['quantity']
            shoe_id = data['shoe_id']
            status = data['status']
            # user_id = data['user_id'] # Redundant 

            shoeObj = ProductsTable.objects.get(id=shoe_id)
            userObj = UserTable.objects.get(unique_id=uid)
            chosenTotalPrice = Decimal(shoeObj.product_price) * Decimal(quantity)
            t = ShoppingCartTable.objects.create(user = userObj, product = shoeObj, quantity = quantity, size = size, color = color, total_price = chosenTotalPrice, status = status)
            t.save

            # Insert Shoe here 
            return JsonResponse('Shoe Added', safe=False)
        else:
            # Not Logged In
            return render(request, 'ShoesInvasionApp/login_user.html')
    except:
        return render(request, 'ShoesInvasionApp/login_user.html')

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
            'status':e.status,
        }
    return render(request, 'ShoesInvasionApp/details.html',context)

def shop(request):
    shoeType = request.GET.get('type', "All Products")
    brand = request.GET.get('brand', "Any")
    gender = request.GET.get('gender', "Any")
    # product = ProductsTable.objects.all
    # No Filter 
    if (shoeType == "All Products" and brand == "Any" and gender == "Any"):
        product = ProductsTable.objects.filter(status=1)
    
    # Filter 
    elif (shoeType == "All Products" and brand != "Any" and gender != "Any" ):
        product = ProductsTable.objects.filter(product_brand = brand, gender_type = gender, status=1)
    elif (shoeType == "All Products" and brand == "Any" and gender != "Any" ):
        product = ProductsTable.objects.filter(gender_type = gender, status=1)
    elif (shoeType == "All Products" and brand != "Any" and gender == "Any" ):
        product = ProductsTable.objects.filter(product_brand = brand, status=1)

    elif (shoeType != "All Products" and brand == "Any" and gender == "Any" ):
        product = ProductsTable.objects.filter(product_category = shoeType, status=1)
    elif (shoeType != "All Products" and brand != "Any" and gender == "Any"):
        is_exist = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, status=1).exists()
        if (is_exist == False):
            product = None
        else:
            product = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, status=1)

    elif (shoeType != "All Products" and brand != "Any" and gender != "Any"):
        product = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, gender_type = gender, status=1)
    elif (shoeType != "All Products" and brand == "Any" and gender != "Any"):
        product = ProductsTable.objects.filter(product_category = shoeType,gender_type = gender, status=1)
    else:
        product = None

    context = {
        'product':product,
        'type':shoeType,
        'gender':brand,
        'brand' : gender, 
    }
    return render(request, 'ShoesInvasionApp/shop.html',context)

def profilePage(request):
    try:
        if request.session.has_key('unique_id'):
            # Logged In
            uid = request.session['unique_id']
            print(uid)
            # uid = request.session.get('unique_id')
            userObj = UserTable.objects.get(unique_id=uid)
            userDetailsObj = UserDetailsTable.objects.get(unique_id=uid)
            context = {
                'firstname': userObj.first_name,
                'lastname': userObj.last_name,
                'username': userObj.username,
                'email': userObj.email,
                'phone': userObj.phone,
                'address': userDetailsObj.address,
            }
            return render(request, 'ShoesInvasionApp/user-profile.html', context=context)
        else:
            # Not Logged In
            return redirect('login/')
            #return HttpResponseRedirect(request=request,template_name="ShoesInvasionApp/login_user.html") | Cannot work
    except:
        # Log 
        # Redirect cause some error occured.
        return redirect('login/')

def viewUpdateProfilePage(request):
    try:
        if request.session.has_key('unique_id'):
            # Logged In
            uid = request.session['unique_id']
            print(uid)
            # uid = request.session.get('unique_id')
            userObj = UserTable.objects.get(unique_id=uid)
            userDetailsObj = UserDetailsTable.objects.get(unique_id=uid)
            context = {
                'firstname': userObj.first_name,
                'lastname': userObj.last_name,
                'username': userObj.username,
                'email': userObj.email,
                'phone': userObj.phone,
                'address': userDetailsObj.address,
            }
            return render(request, 'ShoesInvasionApp/update-profile.html', context=context)
        else:
            # Not Logged In
            return redirect('login/')
    except:
        # Log 
        # Redirect cause some error occured.
        return redirect('login/')

def updateProfileDetails(request):
    # Check for session | Logged In or Not
    try:
        uid = ""
        if request.session.has_key('unique_id'):
            uid = request.session['unique_id']
            data = json.loads(request.body)
            fname = data['fname']
            lname = data['lname']
            phone = data['phone']
            address = data['address']

            if (fname == "" or lname == "" or phone == "" or address == ""):
                return redirect('profilePage')


            userDetailObj = UserDetailsTable.objects.get(unique_id = uid)
            userObj = UserTable.objects.get(unique_id = uid)
            userDetailObj.address = address
            userDetailObj.save()

            userObj.first_name = fname
            userObj.last_name = lname
            userObj.phone = phone
            
            userObj.save()
            return JsonResponse('Update Success', safe=False)
        else:
            # No UID 
            return redirect('login/')
    except:
        # Log Error Message 
        return JsonResponse('Exception Error', safe=False)

def login_request(request):
    if request.session.has_key('unique_id'):
        return render(request, 'ShoesInvasionApp/index.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            otpToken = request.POST['otpToken']
            # need to use HTTP_X_FORWARDED when we deploy, for now its remote addr
            # client_ip=request.META.get('HTTP_X_FORWARDED_FOR')
            client_ip=request.META.get('REMOTE_ADDR')
            try:
                account = UserTable.objects.get(username=username)
                id = account.unique_id
                if (account.accountType == 'User' and account.lockedStatus == 0):
                    if checkPassword(password, account.password):
                        # 2FA not enabled, can login
                        if (account.secret_key == ""):
                            # Right Password | Change Locked Counter to 0
                            account.lockedCounter = 0
                            account.save()
                            # Store into Session
                            request.session['unique_id'] = account.unique_id
                            request.session.set_expiry(900)
                            request.session['secret_key'] = account.secret_key
                            print(client_ip, "passsss")
                            logger.info(f"Successful login by {id} from {client_ip} at time:")
                            return render(request, 'ShoesInvasionApp/index.html')
                        # Got 2FA Enabled
                        else:
                            otpToken = request.POST['otpToken']
                            if (otpToken == None):
                                return render(request, 'ShoesInvasionApp/index.html')
                            else:
                                userSecretKey = pyotp.TOTP(account.secret_key)
                                if (userSecretKey.verify(otpToken)):
                                    # Right Password | Change Locked Counter to 0
                                    account.lockedCounter = 0
                                    account.save()
                                    # Store into Session
                                    request.session['unique_id'] = account.unique_id
                                    request.session.set_expiry(900)
                                    request.session['secret_key'] = account.secret_key
                                    logger.info(f"Successful login by {id} from {client_ip} at time:")
                                    return render(request, 'ShoesInvasionApp/index.html')
                                else:
                                    form = UserLoginForm()
                                    return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form})
                    else:
                        # Wrong Password | Need to append into Locked Counter
                        account.lockedCounter += 1
                        # Once Locked Counter = 3, Lock Account 
                        if (account.lockedCounter == 3):
                            account.lockedStatus = 1
                        account.save()
                        form = UserLoginForm()
                        logger.info(f"Failed login attempt by {id} from {client_ip} (Attempt {account.lockedCounter}) at time:")
                        return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form})

                else:
                    # Wrong Account type. 
                    return render(request, 'ShoesInvasionApp/index.html')

            except UserTable.DoesNotExist:
                return render(request, 'ShoesInvasionApp/register.html')
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
    return render(request, 'ShoesInvasionApp/register_fail.html')

def logout(request):
   try:
      del request.session['unique_id']
    # Used to delete session from database so wont be able to access anymore
    # If login again, it will create a new session
      request.session.flush()
   except:
      pass
   return render(request, 'ShoesInvasionApp/index.html')

def preOrder(request):
    shoeType = request.GET.get('type', "All Products")
    brand = request.GET.get('brand', "Any")
    gender = request.GET.get('gender', "Any")
    # product = ProductsTable.objects.all
    # No Filter 
    if (shoeType == "All Products" and brand == "Any" and gender == "Any"):
        product = ProductsTable.objects.filter(status= 2)
    else:
        product = None

    context = {
        'product':product,
        'type':shoeType,
        'gender':brand,
        'brand' : gender, 
        'status': 2,
    }
    return render(request, 'ShoesInvasionApp/preorder.html',context)
def user_2fa(request):
    context = {}
    if request.method == "POST":
        # Checked
        if 'enable2FA' in request.POST:
            # Get user unique ID
            userDetails = UserTable.objects.get(unique_id=request.session['unique_id'])
            # pyotp generates a random key that is assigned to user and save in db
            userSecretKey = pyotp.random_base32()
            userDetails.secret_key = userSecretKey
            userDetails.save()
            # Create url for qrcode
            url = pyotp.totp.TOTP(userSecretKey).provisioning_uri(name=userDetails.username, issuer_name='ShoesInvasion')
            factory = qrcode.image.svg.SvgImage
            img = qrcode.make(url, image_factory=factory, box_size=20)
            stream = BytesIO()
            img.save(stream)
            context["svg"] = stream.getvalue().decode()
            return render(request,"ShoesInvasionApp/user-2fa.html", context=context)
        # Not checked
        else:
            return render(request, 'ShoesInvasionApp/user-2fa.html')
    else:
        return render(request, 'ShoesInvasionApp/user-2fa.html')
