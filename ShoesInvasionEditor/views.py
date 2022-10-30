from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.urls import reverse
from requests import request
import requests
from ShoesInvasionApp.models.user import  UserTable
from ShoesInvasionApp.models.products import  ProductsTable
from ShoesInvasionApp.models.productQuantity import ProductQuantityTable 
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from ShoesInvasionEditor.forms import createProductForm, updateProductForm, UserLoginForm


def login(request):
    try:
        if (check_login_status(request) == False):
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                response = request.POST['g-recaptcha-response']
                if len(response) == 0:
                        form = UserLoginForm()
                        return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Kindly complete the captcha."})
                account = UserTable.objects.get(username=username)
                
                if (account.accountType == 'Editor' and account.lockedStatus == 0):
                    if checkPassword(password, account.password):
                        # Right Password | Change Locked Counter to 0
                        account.lockedCounter = 0
                        account.save()
                        # Store into Session
                        request.session['unique_id'] = account.unique_id
                        return HttpResponseRedirect('manage')
                    else:
                        # Wrong Password | Need to append into Locked Counter
                        account.lockedCounter += 1
                        # Once Locked Counter = 3, Lock Account 
                        if (account.lockedCounter == 3):
                            account.lockedStatus = 1
                        account.save()
                        form = UserLoginForm()
                        return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
                else:
                    # Wrong Account type. 
                    form = UserLoginForm()
                    return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
            else:
                form = UserLoginForm()
                return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form})
        else:
            # Already Logged in but trying to access login page again
            return HttpResponseRedirect('manage')
    except UserTable.DoesNotExist:
            form = UserLoginForm()
            return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
    except:
            form = UserLoginForm()
            return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
        
def manage(request):
    # Check if logged in
    if (check_login_status(request) == False):
        return HttpResponseRedirect('login')

    # Retrieve all User Info 
    allProdObjs = ProductsTable.objects.all()

    dictArray = []
    for products in allProdObjs:
        # Store Required Data inside Dictionary 
        mydict = {
            "product_id": products.id, 
            "name":products.product_name, 
            "price":products.product_price, 
            "category": products.product_category, 
            "available":products.available, 
            "status":products.status, 
            "brand":products.product_brand
        }
        dictArray.append(mydict)
    context = {
        'data':dictArray
    }
    return render(request, 'ShoesInvasionEditor/products.html', context=context)

def create(request):
    # Check if logged in
    if (check_login_status(request) == False):
        return HttpResponseRedirect('login')

    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_info = request.POST['product_info']
        product_brand = request.POST['product_brand']
        available = request.POST['available']
        gender = request.POST['gender']
        category = request.POST['category']
        # Create Product obj
        newProductObj = ProductsTable.objects.create(product_name = product_name, product_price = product_price, product_info=product_info, product_brand=product_brand, 
        status = available, available = "Yes",gender_type = gender, product_category = category)
        # Save 
        newProductObj.save()
        # data = {"status":"Success", "message":"Insert Successful"}
        # return JsonResponse(data, safe=False)
        return HttpResponseRedirect('manage')

    else:
        form = createProductForm()
        return render(request=request, template_name="ShoesInvasionEditor/insertProducts.html", context={"create_form":form})

def updateProduct(request, pk):
    # Check if logged in
    if (check_login_status(request) == False):
        return HttpResponseRedirect('../../login')
    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_info = request.POST['product_info']
        product_brand = request.POST['product_brand']
        status = request.POST['status']
        gender = request.POST['gender_type']
        category = request.POST['product_category']
        product = ProductsTable.objects.get(id=pk)
        product.product_name = product_name
        product.product_price = product_price
        product.product_info = product_info
        product.product_brand = product_brand
        product.status = status
        product.gender_type = gender
        product.product_category = category

        product.save()
        return HttpResponseRedirect('../../manage')

    else:
        product = ProductsTable.objects.get(id=pk)
        # print("Product is")
        print(product)
        form = updateProductForm(instance=product)
        context={'create_form':form}
        return render(request, template_name="ShoesInvasionEditor/insertProducts.html", context = context)


# products
def remove(request):
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        productObj = ProductsTable.objects.get(id = product_id)
        print(productObj)
        if (productObj.available == "Yes"):
            productObj.available = "No"
            productObj.save()
            data = {"status":"Success", "message":"Product made Unavailable!"}
        elif (productObj.available == "No"):
            productObj.available = "Yes"
            productObj.save()
            data = {"status":"Success", "message":"Product made Available!"}
        else:
            # Error 
            data = {"status":"Failed", "message":"Unable to modify product. Please contact developer for assistance."}
        return JsonResponse(data, safe=False)

    except ObjectDoesNotExist:
    # UID is wrong
        data = {"status":"Failed", "message":"Unable to modify product. Please contact developer for assistance."}
        return JsonResponse(data, safe=False)

    except:
        data = {"status":"Failed", "message":"Unable to modify product. Please contact developer for assistance."}
        return JsonResponse(data, safe=False)


def check_login_status(request):
    try:
        if request.session.has_key('unique_id'):
            uid = request.session['unique_id']
            # Check if uid exist inside db and its admin
            userObj = UserTable.objects.get(unique_id = uid)
            if userObj.accountType == "Editor":
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
        if (account.accountType == 'Editor' and account.lockedStatus == 0):
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

