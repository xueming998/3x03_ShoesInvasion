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
from ShoesInvasionEditor.forms import createProductForm, updateProductForm, EditorLoginForm

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
                if len(response) == 0:
                        form = EditorLoginForm()
                        return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Kindly complete the captcha."})
                account = UserTable.objects.get(username=username)
                
                if (account.accountType == 'Editor' and account.lockedStatus == 0):
                    if checkPassword(password, account.password):
                        # 2FA not enabled, can login
                            if (account.secret_key == ""):
                                # Right Password | Change Locked Counter to 0
                                account.lockedCounter = 0
                                account.save()
                                # Store into Session
                                request.session['unique_id'] = account.unique_id
                                request.session.set_expiry(900)
                                return HttpResponseRedirect('manage')
                            # Got 2FA Enabled
                            else:
                                otpToken = request.POST['otpToken']
                                if (otpToken == None):
                                    form = EditorLoginForm()
                                    return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Enabled OTP cannot be empty."})
                                else:
                                    userSecretKey = pyotp.TOTP(account.secret_key)
                                    if (userSecretKey.verify(otpToken)):
                                        # Right Password | Change Locked Counter to 0
                                        account.lockedCounter = 0
                                        account.save()
                                        # Store into Session
                                        request.session['unique_id'] = account.unique_id
                                        request.session.set_expiry(900)
                                        return HttpResponseRedirect('manage')
                                    else:
                                        form = EditorLoginForm()
                                        return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Incorrect OTP."})
                    else:
                        # Wrong Password | Need to append into Locked Counter
                        account.lockedCounter += 1
                        # Once Locked Counter = 3, Lock Account 
                        if (account.lockedCounter == 3):
                            account.lockedStatus = 1
                        account.save()
                        form = EditorLoginForm()
                        return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
                else:
                    # Wrong Account type. 
                    form = EditorLoginForm()
                    return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
            else:
                form = EditorLoginForm()
                return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form})
        else:
            # Already Logged in but trying to access login page again
            return HttpResponseRedirect('manage')
    except UserTable.DoesNotExist:
            form = EditorLoginForm()
            return render(request=request, template_name="ShoesInvasionEditor/login.html", context={"login_form":form, "status":"Failed", "message":"Username or Password is Incorrect."})
    except:
            form = EditorLoginForm()
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
        status = request.POST['status']
        gender = request.POST['gender']
        category = request.POST['category']
        # Create Product obj
        newProductObj = ProductsTable.objects.create(product_name = product_name, product_price = product_price, product_info=product_info, product_brand=product_brand, 
        status = status, available = "Yes",gender_type = gender, product_category = category, review=5)
        # Save 
        newProductObj.save()
        product_id = ProductsTable.objects.latest('id')
        dictArr = [{"size":"UK 7","quantity":87, "color":"Black", "product_id": product_id}, 
        {"size":"UK 8","quantity":77, "color":"Green", "product_id": product_id}, 
        {"size":"UK 9","quantity":67, "color":"Blue", "product_id": product_id}]
        for x in range(3):
            print(dictArr[x])
            newProductDetailObj = ProductQuantityTable.objects.create(size = dictArr[x]['size'], quantity =dictArr[x]['quantity'], color=dictArr[x]['color'], product = product_id )
            newProductDetailObj.save()
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

def logout(request):
   try:
      del request.session['unique_id']
    # Used to delete session from database so wont be able to access anymore
    # If login again, it will create a new session
      request.session.flush()
      return HttpResponseRedirect('../index')
   except:
      pass
      return HttpResponseRedirect('../index')

def twoFA(request):
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
            return render(request,"ShoesInvasionEditor/twoFA.html", context=context)
        # Not checked
        else:
            return render(request, 'ShoesInvasionEditor/twoFA.html')
    else:
        return render(request, 'ShoesInvasionEditor/twoFA.html')


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request,*args, **argv):
    return render(request, '500.html', status=500)

def unauthorized_view(request,*args, **argv):
    return render(request, '401.html', status=401)

def bad_gateway_view(request,*args, **argv):
    return render(request, '502.html', status=502)