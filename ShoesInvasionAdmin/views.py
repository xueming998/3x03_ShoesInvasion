from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.urls import reverse
from requests import request
import requests
from ShoesInvasionApp.models.user import UserTable 
from ShoesInvasionApp.models.userDetails import UserDetailsTable 
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize


def login(request):
    return render(request, 'ShoesInvasionAdmin/login.html')
    # if (check_login_status(request) == False):
    #     return render(request, 'ShoesInvasionAdmin/login.html')
    # elif (check_login_status(request) == True):
    #     return redirect('manage')

def manage(request):
    # Check if logged in
    if (check_login_status(request) == False):
        return HttpResponseRedirect('login')

    
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
    print(dictArray)
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
        else:
            return False
    except ObjectDoesNotExist:
        # UID is wrong
        return redirect('login')


def checkPassword(password, hashedPassword):
    if check_password(password, hashedPassword):
        print("True")
        return True
    else:
        print("False")
        return False

def checkCaptcha(response_id):
    url  = "https://www.google.com/recaptcha/api/siteverify"
    myobj  = {'secret':'6LeT_rciAAAAACCmGM-MTK9x5Pogedk3VUMV8c0T', 'response':response_id}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    result = requests.post(url, headers=headers,data = myobj)
    result_json = result.json()
    print(result_json)
    print(result_json['success'])
    if result_json['success'] == False:
        return 1
    else:
        return 0

def admin_login(request):
    try:
        # Check if Logined alr. Cannot Access here if so 
        data = json.loads(request.body)
        username = data['username']
        pw = data['pw']
        response = data['g-recaptcha-response']
        if len(response) == 0:
            return JsonResponse('Login Failed', safe=False)
        else:
            # Check Code is valid or not
            valid_status = checkCaptcha(response)
            print(valid_status)
            if valid_status != 0:
                # Response Code Error
                return JsonResponse('Login Failed', safe=False)

            # Empty 
        print("username: "+ username)
        print("pw: "+ pw) 
        # print("g-recaptcha-response: "+  data['g-recaptcha-response'] )
        # Simple Validation if empty string is passed
        if (username == "" or pw == ""):
                return redirect('login')

        account = UserTable.objects.get(username=username)
        print(account.unique_id)
        if (account.accountType == 'Admin' and account.lockedStatus == 0):
            if checkPassword(pw, account.password):
                # Right Password | Change Locked Counter to 0
                    account.lockedCounter = 0
                    account.save()
                    # Store into Session
                    request.session['unique_id'] = account.unique_id
                    # Render to index page
                    return JsonResponse('Login Success', safe=False)
                    # return render(request, 'ShoesInvasionAdmin/index.html')
            else:
                # Wrong Password | Need to append into Locked Counter
                account.lockedCounter += 1
                # Once Locked Counter = 3, Lock Account 
                if (account.lockedCounter == 3):
                    account.lockedStatus = 1
                account.save()
                return JsonResponse('Login Failed', safe=False)
                # return render(request, 'ShoesInvasionAdmin/login.html')
        else:
            return JsonResponse('Login Failed', safe=False)
    
    except UserTable.DoesNotExist:
        # Error 403
        return JsonResponse('Login Failed', safe=False)
    except:
        return JsonResponse('Login Failed', safe=False)

def ban_unban(request):
    try:
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

