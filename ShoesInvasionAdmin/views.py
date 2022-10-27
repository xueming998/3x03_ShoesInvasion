from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from requests import request
import requests
from ShoesInvasionApp.models.user import UserTable 
from ShoesInvasionApp.models.userDetails import UserDetailsTable 
from django.contrib.auth.hashers import check_password

def login(request):
    return render(request, 'ShoesInvasionAdmin/login.html')
    
def index(request):
    return render(request, 'ShoesInvasionAdmin/index.html')
    
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
        data = json.loads(request.body)
        username = data['username']
        pw = data['pw']
        response = data['g-recaptcha-response']
        if len(response) == 0:
            return JsonResponse('Login Failed', safe=False)
        else:
            # Check Code is valid or not
            valid_status = checkCaptcha(response)
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
    except:
        return redirect('login')
