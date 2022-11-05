from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.urls import reverse
from requests import request
import requests, string, secrets
from ShoesInvasionApp.models.user import UserTable 
from ShoesInvasionApp.models.userDetails import UserDetailsTable 
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from ShoesInvasionAdmin.forms import AdminLoginForm, RegisterEditorForm
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password

import logging
logger=logging.getLogger('admins')
validationlogger=logging.getLogger('inputvalidation')

# Import for 2FA
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO

def login(request):
    try:
        if (check_login_status(request) == False):
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                response = request.POST['g-recaptcha-response']
                print("Response Below")
                print(response)
                # need to use HTTP_X_FORWARDED when we deploy, for now its remote addr
                # client_ip=request.META.get('HTTP_X_FORWARDED_FOR')
                client_ip=request.META.get('HTTP_X_FORWARDED_FOR')
                if client_ip:
                    client_ip = client_ip.split(',')[-1].strip()
                else:
                    client_ip=request.META.get('REMOTE_ADDR')
                if len(response) == 0:
                        print("Inside IF ")
                        form = AdminLoginForm()
                        logger.warning(f"Failed administrator login attempt by {username} from {client_ip} with no captcha provided at")
                        return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Kindly complete the captcha."})
                account = UserTable.objects.get(username=username)
                id = account.unique_id
                if (account.accountType == 'Admin' and account.lockedStatus == 0):
                    if (len(password) < 12):
                        form = AdminLoginForm()
                        return render(request=request, template_name="ShoesInvasionApp/login.html", context={"login_form":form, "status":"Failed", "message":"Password have to be at least 12 characters long."})
                    else:
                        if checkPassword(password, account.password):
                            # 2FA not enabled, can login
                            if (account.secret_key == "" or account.secret_key == None):
                                # Right Password | Change Locked Counter to 0
                                account.lockedCounter = 0
                                account.save()
                                # Store into Session
                                request.session['unique_id'] = account.unique_id
                                request.session.set_expiry(900)
                                # request.session['secret_key'] = account.secret_keys
                                logger.info(f"Successful administrator login by {id} from {client_ip} at")
                                return HttpResponseRedirect('manage')
                            # Got 2FA Enabled
                            else:
                                otpToken = request.POST['otpToken']
                                if (otpToken == None):
                                    form = AdminLoginForm()
                                    logger.warning(f"Missing OTP input by administrator {id} from {client_ip} at")
                                    return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Please Enter OTP."})
                                else:
                                    adminSecretKey = pyotp.TOTP(account.secret_key)
                                    if (adminSecretKey.verify(otpToken)):
                                        # Right Password | Change Locked Counter to 0
                                        account.lockedCounter = 0
                                        account.save()
                                        # Store into Session
                                        request.session['unique_id'] = account.unique_id
                                        request.session.set_expiry(900)
                                        logger.info(f"Successful administrator login by {id} from {client_ip} at")
                                        return HttpResponseRedirect('manage')
                                    else:     
                                        form = AdminLoginForm()
                                        logger.critical(f"Failed administrator login attempt by {id} from {client_ip} (Attempt {account.lockedCounter}) at")
                                        return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Incorrect OTP."})
                        else:
                            # Wrong Password | Need to append into Locked Counter
                            account.lockedCounter += 1
                            # Once Locked Counter = 3, Lock Account 
                            if (account.lockedCounter == 3):
                                account.lockedStatus = 1
                                logger.critical(f"Administrator account ({id}) from {client_ip} locked out at time:")
                            account.save()
                            form = AdminLoginForm()
                            logger.critical(f"Failed administrator login attempt by {id} from {client_ip} (Attempt {account.lockedCounter}) at")
                            return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
                        
                else:
                    # Wrong Account type. 
                    form = AdminLoginForm()
                    logger.warning(f"Failed administrator login attempt with non-registered user: {username} from {client_ip} at")
                    return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
            else:
                form = AdminLoginForm()
                return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form})
        else:
            # Already Logged in but trying to access login page again
            return HttpResponseRedirect('manage')
    except UserTable.DoesNotExist:
            form = AdminLoginForm()
            logger.warning(f"Failed administrator login attempt with non-registered user: {username} from {client_ip} at")
            return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
    except:
            form = AdminLoginForm()
            return render(request=request, template_name="ShoesInvasionAdmin/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
 
def manage(request):
    # Check if logged in
    if (check_login_status(request) == False):
        return HttpResponseRedirect('logout/')
    else:
        # Retrieve all User Info 
        allUserObjs = UserTable.objects.all().exclude(accountType = "Admin")
        
        dictArray = []
        for user in allUserObjs:
            # Store Required Data inside Dictionary 
            if (user.accountType == "User" or user.accountType == "Editor"):
                mydict = {
                    "uid": user.unique_id, 
                    "username":user.username, 
                    "lname":user.last_name, 
                    "verifiedStatus": user.verifiedStatus, 
                    "lockedStatus":user.lockedStatus, 
                    "accountType":user.accountType, 
                }
                dictArray.append(mydict)
        context = {
            'data':dictArray
        }
        return render(request, 'ShoesInvasionAdmin/user.html', context=context)

def check_login_status(request):
    try:
        if request.session.has_key('unique_id'):
            uid = request.session['unique_id']
            # Check if uid exist inside db and its admin
            userObj = UserTable.objects.get(unique_id = uid)
            if userObj.accountType == "Admin":
                return True
            else:
                return False
                # Other Account Accessing.
                del request.session['unique_id']
                # Used to delete session from database so wont be able to access anymore
                # If login again, it will create a new session
                request.session.flush()
                return HttpResponseRedirect('logout')
        else:
            return False
    except ObjectDoesNotExist:
        # UID is wrong
        return redirect('login')

def checkPassword(password, hashedPassword):
    if check_password(password, hashedPassword):
        return True
    else:
        return False

def checkCaptcha(response_id):
    url  = "https://www.google.com/recaptcha/api/siteverify"
    myobj  = {'secret':'6LeT_rciAAAAACCmGM-MTK9x5Pogedk3VUMV8c0T', 'response':response_id}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    result = requests.post(url, headers=headers,data = myobj)
    result_json = result.json()
    if result_json['success'] == False:
        return 1
    else:
        return 0

def ban_unban(request):
    try:
        if (check_login_status(request) == True):
            data = json.loads(request.body)
            uid = data['uid']
            accountObj = UserTable.objects.get(unique_id=uid)
            if (accountObj.lockedStatus == 0):
                # Ban
                accountObj.lockedCounter = 3
                accountObj.lockedStatus = 1
                accountObj.save()
            else:
                # unban
                accountObj.lockedStatus = 0
                accountObj.lockedCounter = 0
                accountObj.save()
            data = {"status":"Success", "message":"Ban Successful"}
            return JsonResponse(data, safe=False)
        else:
            data = {"status":"Failed", "message":"logout"}
            return JsonResponse(data, safe=False)
    except UserTable.DoesNotExist:
        # Error 403
        return JsonResponse('Failed Does not exist', safe=False)
    except:
        return JsonResponse('Failed', safe=False)

def logout(request):
   try:
      del request.session['unique_id']
    # Used to delete session from database so wont be able to access anymore
    # If login again, it will create a new session
      request.session.flush()
      return HttpResponseRedirect('../login')
   except:
      pass
      return HttpResponseRedirect('../login')


def twoFA(request):
    # need Check if Logged In or Not (And as Admin or Not)
    if (check_login_status(request) == False):
        return HttpResponseRedirect('logout')
    else:
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
                return render(request,"ShoesInvasionAdmin/twoFA.html", context=context)
            # Not checked
            else:
                return render(request, 'ShoesInvasionAdmin/twoFA.html')
        else:
            return render(request, 'ShoesInvasionAdmin/twoFA.html')

def createEditorAccount(request):
    # Check if logged in
    if (check_login_status(request) == False):
        return HttpResponseRedirect('logout/')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        verify_password = request.POST['verify_password']
        email = request.POST['email']
        phone = request.POST['phone']
        if UserTable.objects.filter(username=username).exists():
            form = RegisterEditorForm()
            return render(request=request, template_name="ShoesInvasionAdmin/create-editor-account.html", 
            context={"create_form":form, "status":"Failed", "message":"Username already exist."})
        else:
            if UserTable.objects.filter(email=email).exists():
                form = RegisterEditorForm()
                return render(request=request, template_name="ShoesInvasionAdmin/create-editor-account.html", 
                context={"create_form":form, "status":"Failed", "message":"Email already exist."})
            else:
                if UserTable.objects.filter(phone=phone).exists():
                    form = RegisterEditorForm()
                    return render(request=request, template_name="ShoesInvasionAdmin/create-editor-account.html", 
                    context={"create_form":form, "status":"Failed", "message":"Phone Number already registered."})
                else:
                    if (password != verify_password):
                        form = RegisterEditorForm()
                        return render(request=request, template_name="ShoesInvasionAdmin/create-editor-account.html", 
                        context={"create_form":form, "status":"Failed", "message":"Password does not match."})
                    else:
                        unique = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range (200))
                        hashedPW = make_password(password)
                        hashedVPW = make_password(verify_password)
                        # Create Account obj
                        accountObj = UserTable.objects.create(first_name = first_name, last_name = last_name, username=username, password=hashedPW, 
                        verify_password = hashedVPW, email = email, phone = phone, bannedStatus = 0, verifiedStatus = 1, verificationCode = 0,
                        lockedStatus = 0, lockedCounter = 0, accountType = "Editor", unique_id = unique, secret_key="")
                        # Save 
                        accountObj.save()
                        # data = {"status":"Success", "message":"Insert Successful"}
                        # return JsonResponse(data, safe=False)
                        return HttpResponseRedirect('manage')

    else:
        form = RegisterEditorForm()
        return render(request=request, template_name="ShoesInvasionAdmin/create-editor-account.html", context={"create_form":form})