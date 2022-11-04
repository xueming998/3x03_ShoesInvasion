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
from django.core.exceptions import ObjectDoesNotExist
from ShoesInvasionApp.forms import RegisterForm
from ShoesInvasionApp.forms import UserLoginForm
from .models.user import UserTable 
from .models.userDetails import UserDetailsTable

from ShoesInvasionApp.models import user as helps
from ShoesInvasionApp.models import transactionDetails
from ShoesInvasionApp.models import transaction

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

# Import for login
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

#Import for Email Validation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
# Import for 2FA
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO
from ShoesInvasionApp.forms import updateProfileForm

#Import for Logging
import logging
logger=logging.getLogger('user')
validationlogger=logging.getLogger('inputvalidation')
#from ShoesInvasionApp import signals

# Create your views here.
def index(request):
        return render(request, 'ShoesInvasionApp/index.html')

def about(request):
    return render(request, 'ShoesInvasionApp/about.html')

def cart(request):
    try:
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout') 
            else:
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
            return HttpResponseRedirect('login')
    except:
        return HttpResponseRedirect('login')

# API CALL POINT 
def update_cartItem(request):
    try:
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout')
            else: 
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
            return HttpResponseRedirect('login')

    except:
        return HttpResponseRedirect('login')

def del_cartItem(request):
    try:
        # Ensure only deleting when logged in
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout')
            else: 
                data = json.loads(request.body)
                shoppingCartID = data['shoppingCartID']
                cartItem = ShoppingCartTable.objects.get(id = shoppingCartID)
                cartItem.delete()

                return JsonResponse('Item was deleted', safe=False)
        else:
            return HttpResponseRedirect('login')
    except:
        return HttpResponseRedirect('login')

def checkout_cartItem(request):
    try:
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout')
            else: 
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
            return HttpResponseRedirect('login')
    except:
        return HttpResponseRedirect('login')

def add_to_cart(request):
    try:
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout')
            else: 
                print("Unique",request.session.get('unique_id'))
                uid = request.session['unique_id']
                data = json.loads(request.body)
                print("Unique", data)
                color = data['color']
                size = data['size']
                quantity = data['quantity']
                shoe_id = data['shoe_id']
                status = data['status']

                shoeObj = ProductsTable.objects.get(id=shoe_id)
                userObj = UserTable.objects.get(unique_id=uid)
                chosenTotalPrice = Decimal(shoeObj.product_price) * Decimal(quantity)
                t = ShoppingCartTable.objects.create(user = userObj, product = shoeObj, quantity = quantity, size = size, color = color, total_price = chosenTotalPrice, status = status)
                t.save

                # Insert Shoe here 
                return JsonResponse('Shoe Added', safe=False)
        else:
            # Not Logged In
            return JsonResponse('Shoe Failed', safe=False)
            # return HttpResponseRedirect('login')
    except:
        return JsonResponse('Shoe Failed', safe=False)

# Just to render Payment Success Page
def paymentSuccess(request):
    return render(request, 'ShoesInvasionApp/thankyou.html')

def checkLoginType(request):
    try:
        if request.session.session_key:
        # if request.session_has_key('unique_id'):
            uid = request.session['unique_id']
            # Check if uid exist inside db and its admin
            userObj = UserTable.objects.get(unique_id = uid)
            if userObj.accountType == "User":
                return True
            else:
                return False
        else:
            return False
    except ObjectDoesNotExist:
        # UID is wrong
        return HttpResponseRedirect('logout')

def shoeDetails(request):
    if (checkLoginType(request) == False):
        return HttpResponseRedirect('logout')
    else: 
        shoeId = request.GET.get('id', '1')
        productQuery = ProductsTable.objects.filter(id = shoeId,available="Yes")
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
            list_for_random = range(20)
            list_for_random2 = range(1,3)
            print(shoeId)
            print(type(shoeId))
            context = {
                'shoeId':shoeId,
                'shoeIdInt':int(shoeId),
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
                'list_for_random': list_for_random,
                'list_for_random2': list_for_random2,
            }
        return render(request, 'ShoesInvasionApp/details.html',context)

def shop(request):
    if (checkLoginType(request) == False):
        return HttpResponseRedirect('logout')
    else: 
        shoeType = request.GET.get('type', "All Products")
        brand = request.GET.get('brand', "Any")
        gender = request.GET.get('gender', "Any")
        # No Filter 
        if (shoeType == "All Products" and brand == "Any" and gender == "Any"):
            product = ProductsTable.objects.filter(status=1,available="Yes")
        
        # Filter 
        elif (shoeType == "All Products" and brand != "Any" and gender != "Any" ):
            product = ProductsTable.objects.filter(product_brand = brand, gender_type = gender, status=1,available="Yes")
        elif (shoeType == "All Products" and brand == "Any" and gender != "Any" ):
            product = ProductsTable.objects.filter(gender_type = gender, status=1,available="Yes")
        elif (shoeType == "All Products" and brand != "Any" and gender == "Any" ):
            product = ProductsTable.objects.filter(product_brand = brand, status=1,available="Yes")

        elif (shoeType != "All Products" and brand == "Any" and gender == "Any" ):
            product = ProductsTable.objects.filter(product_category = shoeType, status=1,available="Yes")
        elif (shoeType != "All Products" and brand != "Any" and gender == "Any"):
            is_exist = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, status=1,available="Yes").exists()
            if (is_exist == False):
                product = None
            else:
                product = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, status=1,available="Yes")

        elif (shoeType != "All Products" and brand != "Any" and gender != "Any"):
            product = ProductsTable.objects.filter(product_category = shoeType,product_brand = brand, gender_type = gender, status=1,available="Yes")
        elif (shoeType != "All Products" and brand == "Any" and gender != "Any"):
            product = ProductsTable.objects.filter(product_category = shoeType,gender_type = gender, status=1,available="Yes")
        else:
            product = None

        list_for_random = range(20)

        context = {
            'product':product,
            'type':shoeType,
            'gender':gender,
            'brand' : brand, 
            'list_for_random': list_for_random,
        }
        return render(request, 'ShoesInvasionApp/shop.html',context)

def profilePage(request):
    try:
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout')
            else: 
                # Logged In
                uid = request.session['unique_id']
                userObj = UserTable.objects.get(unique_id=uid)
                print("before userdetails")
                userDetailsObj = UserDetailsTable.objects.get(unique_id=uid)
                print("before context done")
                context = {
                    'firstname': userObj.first_name,
                    'lastname': userObj.last_name,
                    'username': userObj.username,
                    'email': userObj.email,
                    'phone': userObj.phone,
                    'address': userDetailsObj.address,
                }
                print("context done")
                return render(request, 'ShoesInvasionApp/user-profile.html', context=context)
        else:
            # Not Logged In
            return HttpResponseRedirect('login')
    except:
        # Log 
        # Redirect cause some error occured.
        return HttpResponseRedirect('login')
def viewUpdateProfilePage(request):
    try:
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                return HttpResponseRedirect('logout')
            else: 
                # Logged In
                uid = request.session['unique_id']
                # Check if POST OR NOT
                if request.method == 'POST':
                    first_name = request.POST['first_name']
                    last_name = request.POST['last_name']
                    phone = request.POST['phone']
                    username = request.POST['username']
                    userObj = UserTable.objects.get(unique_id=uid)
                    print(userObj)
                    userObj.first_name = first_name
                    userObj.last_name = last_name
                    userObj.phone = phone
                    userObj.username = username
                    userObj.save()
                    return HttpResponseRedirect('profilePage')
                else:
                    userObj = UserTable.objects.get(unique_id=uid)
                    userDetailsObj = UserDetailsTable.objects.get(unique_id=uid)
                    form = updateProfileForm(instance=userObj)
                    context = {
                        'first_name': userObj.first_name,
                        'last_name': userObj.last_name,
                        'email': userObj.email,
                        'phone': userObj.phone,
                        'address': userDetailsObj.address,
                        'updateProfile_form':form, 
                    }
                    return render(request, 'ShoesInvasionApp/update-profile.html', context=context)
        else:
            # Not Logged In
            return HttpResponseRedirect('login')
    except:
        # Log 
        # Redirect cause some error occured.
        return HttpResponseRedirect('login')

def updateProfileDetails(request):
    # Check for session | Logged In or Not
    try:
        uid = ""
        if request.session.has_key('unique_id'):
            if (check_login_status(request) == False):
                # return JsonResponse('Update Login Failed', safe=False)
                return HttpResponseRedirect('logout')
            else: 
                uid = request.session['unique_id']
                data = json.loads(request.body)
                fname = data['fname']
                lname = data['lname']
                phone = data['phone']
                address = data['address']

                if (fname == "" or lname == "" or phone == "" or address == ""):
                    # return JsonResponse('Update Failed', safe=False)
                    return HttpResponseRedirect('profilePage')


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
            # return JsonResponse('Update Login Failed', safe=False)
            return HttpResponseRedirect('login')
    except:
        # Log Error Message 
        return JsonResponse('Exception Error', safe=False)


def check_login_status(request):
    try:
        uid = request.session['unique_id']
        # Check if uid exist inside db and its admin
        userObj = UserTable.objects.get(unique_id = uid)
        if userObj.accountType == "User":
            return True
        else:
            return False
    except ObjectDoesNotExist:
        # UID is wrong
        return HttpResponseRedirect('logout')

def login_request(request):

    if request.session.has_key('unique_id'):
        # Check if Admin or Editor 
        if (check_login_status(request) == False):
            return HttpResponseRedirect('logout') 
        else:
            return HttpResponseRedirect('home') 
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            response = request.POST['g-recaptcha-response']
            print("username: " + username)
            otpToken = request.POST['otpToken']
            # need to use HTTP_X_FORWARDED when we deploy, for now its remote addr
            # client_ip=request.META.get('HTTP_X_FORWARDED_FOR')
            client_ip=request.META.get('REMOTE_ADDR')
            try:
                account = UserTable.objects.get(username=username)
                id = account.unique_id
                if len(response) == 0:
                    form = UserLoginForm()
                    logger.critical(f"No Captcha Done by user at user login attempt by {id} from {client_ip} (Attempt {account.lockedCounter}) at time:")
                    return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form, "error": "Reattempt Captcha."})
                if (account.accountType == 'User' and account.lockedStatus == 0):
                    if (len(password) < 12):
                        form = UserLoginForm()
                        return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form, "error": "Password have to be at least 12 characters long."})
                    else:
                        if (len(otpToken) != 6):
                            form = UserLoginForm()
                            return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form, "error": "OTP Token has to be 6 numbers."})
                        else:
                            if checkPassword(password, account.password):
                                userSecretKey = pyotp.TOTP(account.secret_key)
                                if (userSecretKey.verify(otpToken)):
                                    # Right Password | Change Locked Counter to 0
                                    account.lockedCounter = 0
                                    account.save()
                                    # Store into Session
                                    request.session['unique_id'] = account.unique_id
                                    request.session.set_expiry(900)
                                    request.session['secret_key'] = account.secret_key
                                    logger.info(f"Successful user login by {id} from {client_ip} at time:")
                                    return render(request, 'ShoesInvasionApp/index.html')
                                else:
                                    form = UserLoginForm()
                                    return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form, "error": "Incorrect OTP."})
                            else:
                                # Wrong Password | Need to append into Locked Counter
                                account.lockedCounter += 1
                                # Once Locked Counter = 3, Lock Account 
                                if (account.lockedCounter == 3):
                                    account.lockedStatus = 1
                                    logger.critical(f"User account ({id}) from {client_ip} locked out at time:")
                                account.save()
                                form = UserLoginForm()
                                logger.critical(f"Failed user login attempt by {id} from {client_ip} (Attempt {account.lockedCounter}) at time:")
                                return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form, "error": "Incorrect Username or Password."})

                else:
                    # Wrong Account type. 
                    form = UserLoginForm()
                    logger.critical(f"Failed user login attempt with non-registered user: {id} from {client_ip} (Attempt {account.lockedCounter}) at time:")
                    return render(request, 'ShoesInvasionApp/login_user.html', context={"login_form":form, "error": "Incorrect Username or Password."})

            except UserTable.DoesNotExist:
                form = UserLoginForm()
                logger.critical(f"Failed user login attempt with non-registered user: {id} from {client_ip} (Attempt {account.lockedCounter}) at time:")
                return render(request, 'ShoesInvasionApp/login_user.html', context={"login_form":form, "error": "Incorrect Username or Password."})
            except:
                form = UserLoginForm()
                logger.critical(f"Failed user login attempt with non-registered user: {id} from {client_ip} (Attempt {account.lockedCounter}) at time:")
                return render(request, 'ShoesInvasionApp/login_user.html', context={"login_form":form, "error": "Incorrect Username or Password."})
        else:       
            form = UserLoginForm()
            return render(request=request, template_name="ShoesInvasionApp/login_user.html", context={"login_form":form})

def checkPassword(password, hashedPassword):
    if check_password(password, hashedPassword):
        return True
    else:
        return False  
    
def activate(request, verificationcode,token):    
    try:
        user = UserTable.objects.get(verificationCode=verificationcode)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.verifiedStatus = 1
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return render(request,'ShoesInvasionApp/activation_success.html')
    else:
        messages.error(request, 'Activation link is invalid!')
        return render(request, 'ShoesInvasionApp/register_fail.html')

def activateEmail(request, user,to_email):
    current_site = get_current_site(request)
    subject = 'Activate your ShoesInvasion account today.'
    message = render_to_string('ShoesInvasionApp/email-template.html',
                                {'user': user,
                                'domain':current_site.domain,
                                'uid':user.verificationCode,
                                'token': account_activation_token.make_token(user),
                                'protocol': 'https' if request.is_secure() else 'http'})
    email = EmailMessage(subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
    
def register_request(request):
    if request.session.has_key('unique_id'):
        return HttpResponseRedirect('../home')
    else:
        if request.method == 'POST':
            formDetails = RegisterForm(request.POST)
            if formDetails.is_valid():
                post = formDetails.save(commit = False)
                post.save()
                activateEmail(request,post, formDetails.cleaned_data.get('email'))
                context = {}
                registerEmail = formDetails.cleaned_data['email']
                context['email'] = registerEmail
                # Use email get uid 
                userObj = UserTable.objects.get(email = registerEmail)
                uid = userObj.unique_id
                # store user details inside 
                newUserDetailObj = UserDetailsTable.objects.create(address = "Orchard Rd", date_of_birth="1998-06-21", gender = "Male", unique_id = userObj)
                newUserDetailObj.save()
                return render(request, 'ShoesInvasionApp/register_success.html', context)
            
            else:
                return render(request, 'ShoesInvasionApp/register.html', {'form': formDetails})
        else:
            form = RegisterForm(None)
            return render(request, 'ShoesInvasionApp/register.html', {'form':form})

def registerSuccess(request):
    if request.session.has_key('unique_id'):
        return HttpResponseRedirect('../home')
    else: 
        # Generating QR Code for 2FA
        context = {}
        if request.method == "POST":
                # Get user unique ID
                userDetails = UserTable.objects.get(email=request.POST['email'])
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
                context["email"] = request.POST['email']
                return render(request,"ShoesInvasionApp/register_success.html", context=context)
        else:
            return render(request, 'ShoesInvasionApp/register.html')

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
   return HttpResponseRedirect('home')


def preOrder(request):
    shoeType = request.GET.get('type', "All Products")
    brand = request.GET.get('brand', "Any")
    gender = request.GET.get('gender', "Any")
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

def page_not_found_view(request, exception):
    return render(request, 'ShoesInvasionApp/404.html', status=404)

def server_error_view(request,*args, **argv):
    return render(request, 'ShoesInvasionApp/500.html', status=500)

def unauthorized_view(request,*args, **argv):
    return render(request, 'ShoesInvasionApp/401.html', status=401)

def bad_gateway_view(request,*args, **argv):
    return render(request, 'ShoesInvasionApp/501.html', status=501)