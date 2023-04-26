from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .models import fuelStations
# from app import models
from app.models import fuelStations
from app.models import products
from app.models import jobs
from app.models import reviews
from app.models import cart
from app.models import users
from app.models import applicant
from app.models import myAdmin
from app.models import order
from django.db import connection

import smtplib, ssl
import random

from django.forms.models import model_to_dict

# import firebase_admin
# from firebase_admin import credentials

# import pyrebase

# ===================================================================================================================

smtp_server = "smtp.gmail.com"
port = 587  # For starttls

sender = ''
mail_password = ""

myCart = cart()
cart_product = []



fIdx = 0

# cred = credentials.Certificate('')
# firebase_admin.initialize_app(cred)
# # OR
# firebase_admin.initialize_app(credentials.Certificate('one-planet-fuel-station-firebase-adminsdk-7vkbh-0548d89e33.json'))

# firebaseConfig = {
#   "apiKey": "AIzaSyAduPUg4nBhq9-dDm5cZ1FY6qED7FBrAXs",
#   "authDomain": "onestopfuelstation.firebaseapp.com",
#   "databaseURL": "https://onestopfuelstation-default-rtdb.firebaseio.com",
#   "projectId": "onestopfuelstation",
#   "storageBucket": "onestopfuelstation.appspot.com",
#   "messagingSenderId": "784006978110",
#   "appId": "1:784006978110:web:ac8901ea7e07d65b638f6f",
#   "measurementId": "G-7JLJ91DKKC"
# };

# firebase = pyrebase.initialize_app(firebaseConfig)
# authe = firebase.auth()
# database=firebase.database()

# some useful functions
def getFuelStationName(fs_id):
    try:
        entity = fuelStations.objects.get(id=fs_id)
        return entity.name
    except fuelStations.DoesNotExist:
        return None

def getUserName(usr_id):
    try:
        entity = users.objects.get(id=usr_id)
        return entity.firstName+' '+entity.LastName
    except users.DoesNotExist:
        return None

def getProductTitle(prdct_id):
    try:
        entity = products.objects.get(id=prdct_id)
        return entity.title
    except products.DoesNotExist:
        return None

def getJobName(job_id):
    try:
        entity = jobs.objects.get(id=job_id)
        return entity.job_name
    except jobs.DoesNotExist:
        return None

# Create your views here.
def site(request):
    product_list = products.objects.all()
    station_list = fuelStations.objects.all()
    review_list = reviews.objects.all()

    context = {
        'product_list': product_list,
        'station_list': station_list,
        'review_list': review_list
    }

    return render(request, 'index.html', context)

def demo(request):
    product_list = products.objects.all()
    station_list = fuelStations.objects.all()
    review_list = reviews.objects.all()

    context = {
        'product_list': product_list,
        'station_list': station_list,
        'review_list': review_list,
    }

    return render(request, 'demo.html', context)

def fuelStation_view(request, station_id):
    station = fuelStations.objects.get(pk=station_id)
    orderList = order.objects.all()

    orderNum = 0

    sales = 0

    for ordr in orderList:
        if ordr.fuelStation == station:
            sales += ordr.totalCost
            orderNum = orderNum + 1

    context = {
        'station_id': station_id,
        'station': station,
        'orderList': orderList,
        'orderNum': orderNum,
        'sales': sales,
    }
    print("==========================")
    print("fIdx: ", fIdx)
    print("==========================")

    return render(request, 'dashboard.html', context)

def fuelStationList_view(request):
    station_list = fuelStations.objects.all()

    context = {
        'station_list': station_list
    }

    return render(request, 'StationList.html', context)

def products_view(request):
    product_list = products.objects.all()
    subTotal = 0

    context = {
        'product_list': product_list,
        'filter': False
    }

    # myCart.user.email = "testuser@gmail.com"

    if request.method == 'POST':
        print("Filter")

        fltr = request.POST['Filter']
        crt = request.POST['cart']

        print("Filter - ", fltr)

        if fltr == "Category":
            if crt == '0':
                print("A1: Cart - ", crt)
                context2 = {
                    'product_list': product_list,
                    'filter': False,
                    'subTotal': subTotal
                }
                return render(request, 'Products.html', context2)
            else:
                print("A2: Cart - ", crt)

                p = products.objects.get(pk=crt)
                # myCart.products.add(p)
                cart_product.append(p)

                for pr in cart_product:
                    subTotal += pr.price

                count = len(cart_product)

                context2 = {
                    'product_list': product_list,
                    'filter': False,
                    'pid': crt,
                    'myCart': myCart,
                    'subTotal': subTotal,
                    'cart_product': cart_product,
                    'count': count
                }
                return render(request, 'Products.html', context2)
        else:
            if crt == '0':
                print("B1: Cart - ", crt)

                context2 = {
                    'product_list': product_list,
                    'filter': True,
                    'Fltr_val': fltr
                }
                return render(request, 'Products.html', context2)
            else:
                print("B2: Cart - ", crt)

                p = products.objects.get(pk=crt)
                # myCart.products.add(p)
                cart_product.append(p)

                for pr in cart_product:
                    subTotal += pr.price

                count = len(cart_product)
                
                context2 = {
                    'product_list': product_list,
                    'filter': False,
                    'pid': crt,
                    'myCart': myCart,
                    'subTotal': subTotal,
                    'cart_product': cart_product,
                    'count': count
                }
                return render(request, 'Products.html', context2)

    return render(request, 'Products.html', context)

def products2_view(request, station_id):
    product_list = products.objects.all()
    subTotal = 0

    context = {
        'product_list': product_list,
        'filter': False,
        'station_id': station_id
    }

    # myCart.user.email = "testuser@gmail.com"

    if request.method == 'POST':
        print("Filter")
        print("station_id: ", station_id)
        print("type(station_id): ", type(station_id))


        categoryFilter = request.POST['CategoryFilter']
        crt = request.POST['cart']
        Checkout = request.POST['Checkout']
        
        orderBy = request.POST['OderByFilter']
        priceFilter = request.POST['PriceFilter']

        print("CategoryFilter - ", categoryFilter)
        print("OderByFilter - ", orderBy)
        print("priceFilter - ", priceFilter)
        print("Checkout - ", Checkout)
        print("==========================================")

        if Checkout == "1":
            # subTotal = 0
            context3 = {}

            for pr in cart_product:
                    subTotal += pr.price

            print("-----------------------------")
            print("Checkout")
            print("subTotal: ", subTotal)
            print("-----------------------------")

            context3['subTotal'] = subTotal
            context3['station_id'] = station_id

            URL = '/app/Check-Out/' + str(station_id) + '/' + str(subTotal) + '/'
            return HttpResponseRedirect(URL, context3)

        if orderBy == "Alphabet":
            print("Order product list alphabetically")
            print("1 product_list: ", product_list)
            print("1 type(product_list): ", type(product_list))

            product_list = product_list.order_by('title')

            print("2 product_list: ", product_list)
            print("2 type(product_list): ", type(product_list))

        if priceFilter == "1":
            product_list = product_list.filter(price__lt=1000)
        if priceFilter == "2":
            product_list = product_list.filter(price__gte=1000)
            product_list = product_list.filter(price__lte=2500)
        if priceFilter == "3":
            product_list = product_list.filter(price__gte=2500)
            product_list = product_list.filter(price__lte=3500)
        if priceFilter == "4":
            product_list = product_list.filter(price__gt=3500)

        if categoryFilter == "Category":
            if crt == '0':
                print("A1: Cart - ", crt)
                context2 = {
                    'product_list': product_list,
                    'filter': False,
                    'subTotal': subTotal,
                    'station_id': station_id
                }
                return render(request, 'Products2.html', context2)
            else:
                print("A2: Cart - ", crt)

                p = products.objects.get(pk=crt)
                # myCart.products.add(p)
                cart_product.append(p)

                for pr in cart_product:
                    subTotal += pr.price

                count = len(cart_product)

                context2 = {
                    'product_list': product_list,
                    'filter': False,
                    'pid': crt,
                    'myCart': myCart,
                    'subTotal': subTotal,
                    'cart_product': cart_product,
                    'count': count,
                    'station_id': station_id
                }
                return render(request, 'Products2.html', context2)
        else:
            if crt == '0':
                print("B1: Cart - ", crt)

                context2 = {
                    'product_list': product_list,
                    'filter': True,
                    'Fltr_val': categoryFilter,
                    'station_id': station_id
                }
                return render(request, 'Products2.html', context2)
            else:
                print("B2: Cart - ", crt)

                p = products.objects.get(pk=crt)
                # myCart.products.add(p)
                cart_product.append(p)

                for pr in cart_product:
                    subTotal += pr.price

                count = len(cart_product)
                
                context2 = {
                    'product_list': product_list,
                    'filter': True,
                    'Fltr_val': categoryFilter,
                    'pid': crt,
                    'myCart': myCart,
                    'subTotal': subTotal,
                    'cart_product': cart_product,
                    'count': count,
                    'station_id': station_id
                }
                return render(request, 'Products2.html', context2)

    return render(request, 'Products2.html', context)

def addProduct_view(request, station_id):
    station = fuelStations.objects.get(pk=station_id)
    context = {
        'station_id': station_id,
        'station': station
    }

    print("Add Product")
    print("context['station_id']: ", context['station_id'])
    print("type(context['station_id']): ", type(context['station_id']))

    # User.objects.filter(username=username).exists()
    
    if request.method == 'POST':
        print("This is post - Add product")

        Title = request.POST['Title']
        Description = request.POST['Description']
        Category = request.POST['Category']
        image = request.FILES['image']
        Price = request.POST['Price']
        Details = request.POST['Details']
        # FuelStation = fuelStations.objects.get(pk=station_id)

        print("\t\t========================")
        print("\t\tTitle = ", Title)
        print("\t\tDescription = ", Description)
        print("\t\tCategory = ", Category)
        print("\t\timage = ", image)
        print("\t\tPrice = ", Price)
        print("\t\tDetails = ", Details)
        print("\t\tFuelStation = ", station.name)
        print("\t\t========================\n\n")

        # product_list = products.objects.all()

        query = True

        # for product in product_list:
        #     if product.title == Title:
        #         print("This particular product already exists. Please Enter valid details")
        #         query = False

        # if products.objects.filter(title=Title).exists():
        #     print("Product exists already")
        #     query = False

        if query:
            db_add = products()

            db_add.title = Title
            db_add.description = Description
            db_add.category = Category
            db_add.image = image
            db_add.price = Price
            # db_add.fuelStation = FuelStation
            db_add.fuelStation = station
            
            db_add.save()

            print("Sucessfully added a product!")

            # return render(request, 'Add Products.html', context)
        
        URL = '/app/AddProducts/' + str(station_id) + '/'
        return HttpResponseRedirect(URL, context)
        # return render(request, 'Add Products.html', context)

    return render(request, 'Add Products.html', context)

def reviews_view(request):
    review_list = reviews.objects.all()

    context = {
        'review_list': review_list
    }

    return render(request, 'reviews.html', context)

def contactUs_view(request):
    return render(request, 'Contact Us.html')

def aboutUs_view(request):
    return render(request, 'About Us.html')

def LogIn_view(request):
    context = {}

    if request.method == 'POST':
        print("This is post - Login")

        email = request.POST['email']
        password = request.POST['password']

        # print(email, password)

        station_list = fuelStations.objects.all()

        for station in station_list:
            if station.email == email:
                if station.password == password:
                    print("LogIn Sucessfull hello")
                    print("Station: ", station.name)
                    print("id: ", station.id)

                    context['station_id'] = station.id
                    context['station'] = station
                    # fIdx = station.id
                    # return render(request, 'dashboard.html', context)
                    # return fuelStation_view(request)
                    # return HttpResponseRedirect('/app/FuelStation/{{station.id}}', context)
                    URL = '/app/FuelStation/' + str(station.id) + '/'
                    return HttpResponseRedirect(URL, context)
                else:
                    print("Incorrect Password")
                    return render(request, 'Login F.html', context)
        
        print("Incorrect email")
        return render(request, 'Login F.html', context)

    return render(request, 'Login F.html', context)

def Register_view(request):
    context = {}

    if request.method == 'POST':
        print("This is post - Registration")

        stnName = request.POST['stnName']
        addrs = request.POST['addrs']
        email = request.POST['email']
        phoneNo = request.POST['phoneNo']
        password = request.POST['password']

        # print(stnName, addrs, email, phoneNo, password)

        station_list = fuelStations.objects.all()

        query = True

        for station in station_list:
            if station.email == email:
                print("This particular station already exists. Please Enter valid details")
                query = False

        if query:
            db_add = fuelStations()

            db_add.name = stnName
            db_add.address = addrs
            db_add.email = email
            db_add.phone = phoneNo
            db_add.password = password
            
            db_add.save()

            print("Registration Sucessfull")

            message = """\
Subject: One Planet OTP message

Welcome. Your OTP is: """

            otp = random.randint(100000, 999999)

            context['otp'] = otp
            message += str(otp)

            # Create a secure SSL context
            context2 = ssl.create_default_context()

            # Try to log in to server and send email
            try:
                server = smtplib.SMTP(smtp_server,port)
                server.ehlo() # Can be omitted
                server.starttls(context=context2) # Secure the connection
                server.ehlo() # Can be omitted
                server.login(sender, mail_password)
                # TODO: Send email here
                server.sendmail(sender, email, message)
            except Exception as e:
                # Print any error messages to stdout
                print(e)
            finally:
                server.quit() 

            return render(request, 'validate.html', context)

    return render(request, 'Registration F.html', context)

def RegisterVerify_view(request):
    context = {}

    if request.method == 'POST':
        print("This is post - Validate")

        otp = request.POST['otp']
        originalOTP = request.POST['originalOTP']

        if otp == originalOTP:
            print("Verification Sucessfull")
            return HttpResponseRedirect('/app/LogIn/')
        else:
            context['OTP_status'] = False
            return render(request, 'Registration F.html', context)

    return render(request, 'validate.html', context)

JOB_ID = 0

def Careers_view(request):
    job_list = jobs.objects.all()

    context = {
        'job_list': job_list
    }

    if request.method == 'POST':
        # JobId = request.POST['Jid']
        JOB_ID = request.POST['Jid']

        print("jid: ", JOB_ID)

        # context = {
        #     'JobId': JobId
        # }

        # return render(request, 'JobApply.html', context)
        # JobApply_view(request)
        return redirect('/app/Job-Apply/', job_id=JOB_ID)


    return render(request, 'Careers.html', context)

def PostJobs_view(request, station_id):
    station = fuelStations.objects.get(pk=station_id)
    # context = {
    #     'station_id': station_id,
    #     'station': station
    # }

    station_list = fuelStations.objects.all()
    context = {
        'station_list':station_list
    }

    print("Post Job")
    print("station_id: ", station_id)
    print("type(station_id): ", type(station_id))
    print("station.name: ", station.name)

    context['station_id'] = station_id
    context['station'] = station

    if request.method == 'POST':
        print("This is post - Job Posting")

        JobName = request.POST['JobName']
        Designation = request.POST['Designation']
        stnName = request.POST['stnName']
        # stnAddrs = request.POST['stnAddrs']
        # stnPhone = request.POST['stnPhone']
        JobDetails = request.POST['JobDetails']

        print("\t\t========================")
        print("\t\tJobName = ", JobName)
        print("\t\tDesignation = ", Designation)
        print("\t\tFuelStation = ", stnName)
        # print("\t\tstnName = ", stnName)
        # print("\t\tstnAddrs = ", stnAddrs)
        # print("\t\tstnPhone = ", stnPhone)
        print("\t\tJobDetails = ", JobDetails)
        print("\t\t========================\n\n")

        # job_list = jobs.objects.all()
        # station_list = fuelStations.objects.all()
        Jstation = fuelStations()

        query = False

        # for job in job_list:
        #     if job.fuelStation. == stnName:
        #         print("This particular station already exists. Please Enter valid details")
        #         query = False

        for station in station_list:
            if station.name == stnName:
                Jstation = station
                print("Found station")
                query = True

        if query:
            db_add = jobs()

            db_add.job_name = JobName
            db_add.designation = Designation
            db_add.fuelStation = Jstation
            # db_add. = stnName
            # db_add. = stnAddrs
            # db_add. = stnPhone
            db_add.details = JobDetails
            
            db_add.save()

            print("Job Posted Sucessfully")

            # return render(request, 'Jobs F.html', context)

    return render(request, 'Jobs F.html', context)

def CheckOut_view(request, station_id, amount):
    context = {
        'station_id': station_id,
        'amount': amount
    }

    if request.method == 'POST':
        firstName = request.POST['fnm']
        lastName = request.POST['lnm']
        mail = request.POST['email']
        phone = request.POST['phone']
        station_id = request.POST['station_id']
        amount = request.POST['amount']

        amount = float(amount)

        print("===================================")
        print('email: ', mail)
        print('station_id: ', station_id)
        print('amount: ', amount)
        print('type(amount): ', type(amount))
        print("===================================")

        user_list = users.objects.all()
        shopUser = 0
        # obj = users()

        query = True

        for user in user_list:
            if user.email == mail:
                # print("This particular product already exists. Please Enter valid details")
                shopUser = user
                query = False

        # if products.objects.filter(title=Title).exists():
        #     print("Product exists already")
        #     query = False

        if query:
            db_add = users()

            db_add.firstName = firstName
            db_add.LastName = lastName
            db_add.email = mail
            db_add.phone = phone

            db_add.save()

            shopUser = db_add

        # myCart.user.firstName = firstName
        # myCart.user.LastName = lastName
        # myCart.user.email = mail
        # myCart.user.phone = phone

        # obj = users.objects.filter(email=mail).values

        # if not obj:
        #     obj = users(firstName=firstName, LastName=lastName, email=mail, phone=phone)

        # myCart.user = obj
        # myCart.products = cart_product

        # myCart.save()

        station = fuelStations.objects.get(pk=station_id)

        print("station: ", station)

        newOrder = order()

        newOrder.totalCost = amount
        newOrder.Customer = shopUser
        newOrder.fuelStation = station

        newOrder.save()

        cart_product.clear()

        context = {
            'message': 'Thankyou for your purchase',
            'checkOut': True
        }

        print("Post request made")
        # return HttpResponseRedirect('/app/index/', context)
        return render(request, 'index.html', context)
    
    return render(request, 'CheckOut.html', context)

def JobApply_view(request):
    context = {
        'message': '',
        'apply': False
    }

    if request.method == 'POST':
        # render(request, 'JobApply.html', context)
        # job_id = request.POST['job_id']
        firstName = request.POST['fnm']
        lastName = request.POST['lnm']
        mail = request.POST['email']
        phone = request.POST['phone']

        # print("job_id: ", JOB_ID)
        
        # obj = applicant()

        # obj.job = jobs.objects.get(pk=JOB_ID)
        # obj.user.firstName = firstName
        # obj.user.LastName = lastName
        # obj.user.email = mail
        # obj.user.phone = phone

        context = {
            'message': 'Thankyou for applying - We will get back to you soon!',
            'apply': True
        }

        # obj.save()

        # return render(request, 'index.html', context)
        return HttpResponseRedirect('/app/index/', context)

    return render(request, 'JobApply.html', context)

def AdminLogin(request):
    context = {}

    if request.method == 'POST':
        print("This is post - Login")

        email = request.POST['email']
        password = request.POST['password']

        # print(email, password)

        admin_list = myAdmin.objects.all()

        for admin in admin_list:
            if admin.email == email:
                if admin.password == password:
                    print("Admin LogIn Sucessfull hello")
                    print("admin.email: ", admin.email)
                    print("id: ", admin.id)

                    context['admin_id'] = admin.id
                    context['admin'] = admin
                    # fIdx = station.id
                    # return render(request, 'dashboard.html', context)
                    # return fuelStation_view(request)
                    # return HttpResponseRedirect('/app/FuelStation/{{station.id}}', context)
                    URL = '/app/myAdmin/dashboard/'
                    return HttpResponseRedirect(URL, context)
                else:
                    print("Incorrect Password")
                    return render(request, 'myAdminLogin.html', context)
        
        print("Incorrect email")
        return render(request, 'myAdminLogin.html', context)

    return render(request, 'myAdminLogin.html', context)

def AdminRegistration(request):
    context = {}

    if request.method == 'POST':
        print("This is post - Registration")

        email = request.POST['email']
        password = request.POST['password']

        # print(stnName, addrs, email, phoneNo, password)

        admin_list = myAdmin.objects.all()

        query = True

        for admin in admin_list:
            if admin.email == email:
                print("This particular admin already exists. Please Enter valid details")
                query = False

        if query:
            db_add = myAdmin()

            db_add.email = email
            db_add.password = password
            
            db_add.save()

            print("Registration Sucessfull")

#             message = """\
# Subject: One Planet OTP message

# Welcome. Your OTP is: """

#             otp = random.randint(100000, 999999)

#             context['otp'] = otp
#             message += str(otp)

#             # Create a secure SSL context
#             context2 = ssl.create_default_context()

#             # Try to log in to server and send email
#             try:
#                 server = smtplib.SMTP(smtp_server,port)
#                 server.ehlo() # Can be omitted
#                 server.starttls(context=context2) # Secure the connection
#                 server.ehlo() # Can be omitted
#                 server.login(sender, mail_password)
#                 # TODO: Send email here
#                 server.sendmail(sender, email, message)
#             except Exception as e:
#                 # Print any error messages to stdout
#                 print(e)
#             finally:
#                 server.quit() 

            # return render(request, 'validate.html', context)
            
            URL = '/app/myAdmin/'
            return HttpResponseRedirect(URL, context)

    return render(request, 'myAdminRegistration.html', context)

def AdminSite(request):
    context = {}

    # cursor = connection.cursor()
    # # cursor.execute("SHOW TABLES")
    # tables = cursor.fetchall()

    # table_names = [row[0] for row in tables]

    # context['table_names'] = table_names

    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)

    print("tables: ", tables)
    print("seen_models: ", seen_models)
    print("tables[0]: ", tables[0])
    print("type(tables[0]): ", type(tables[0]))

    tables = [item for item in tables if item.count('_') < 2]
    tables = [item for item in tables if 'auth' not in item]
    tables = [item for item in tables if 'django' not in item]

    for i in range(len(tables)):
        tables[i] = tables[i].replace("app_", "")

    table_names = tables
    
    context['table_names'] = table_names

    return render(request, 'myAdmin.html', context)

def fireBase_test(request):
    context = {}

    return render(request, 'firebaseTest.html', context)

def AdminSiteDetails(request, table_name):
    context = {}

    print("AdminSiteDetails")
    print("table_name: ", table_name)
    
    product_list = products.objects.all()
    station_list = fuelStations.objects.all()
    review_list = reviews.objects.all()
    cart_list = cart.objects.all()
    job_list = jobs.objects.all()
    users_list = users.objects.all()
    applicant_list = applicant.objects.all()
    myAdmin_list = myAdmin.objects.all()
    order_list = order.objects.all()

    # data = table_name.objects.all()

    context['table_name'] = table_name
    # context['product_list'] = product_list
    # context['station_list'] = station_list
    # context['review_list'] = review_list
    # context['cart_list'] = cart_list
    # context['job_list'] = job_list
    # context['users_list'] = users_list
    # context['applicant_list'] = applicant_list
    # context['myAdmin_list'] = myAdmin_list

    if table_name == "fuelstations":
        context['table_data'] = station_list
        print("station_list: ", station_list)

    if table_name == "products":
        context['table_data'] = product_list
        print("product_list: ", product_list)

    if table_name == "reviews":
        context['table_data'] = review_list
        print("review_list: ", review_list)

    if table_name == "cart":
        context['table_data'] = cart_list
        print("cart_list: ", cart_list)

    if table_name == "jobs":
        context['table_data'] = job_list

    if table_name == "users":
        context['table_data'] = users_list

    if table_name == "applicant":
        context['table_data'] = applicant_list
        print("applicant_list: ", applicant_list)

    if table_name == "myadmin":
        context['table_data'] = myAdmin_list
        
    if table_name == "order":
        context['table_data'] = order_list

    return render(request, 'adminTableDetails.html', context)

def AdminSiteAction(request, table_name, action, data_id):
    context = {}

    entity = {}
    entityDataList = []

    print("AdminSiteDetails")
    print("table_name: ", table_name)
    print("action: ", action)
    print("data_id: ", data_id)
    
    product_list = products.objects.all()
    station_list = fuelStations.objects.all()
    review_list = reviews.objects.all()
    cart_list = cart.objects.all()
    job_list = jobs.objects.all()
    users_list = users.objects.all()
    applicant_list = applicant.objects.all()
    myAdmin_list = myAdmin.objects.all()
    order_list = order.objects.all()

    # data = table_name.objects.all()

    context['table_name'] = table_name
    # context['product_list'] = product_list
    # context['station_list'] = station_list
    # context['review_list'] = review_list
    # context['cart_list'] = cart_list
    # context['job_list'] = job_list
    # context['users_list'] = users_list
    # context['applicant_list'] = applicant_list
    # context['myAdmin_list'] = myAdmin_list

    context['action'] = action

    if table_name == "fuelstations":
        context['table_data'] = station_list
        print("station_list: ", station_list)

        if data_id > 0:
            entity = fuelStations.objects.get(pk=data_id)
            
        print('len(fuelStations._meta.get_fields()): ', len(fuelStations._meta.get_fields()))

        # fields = fuelStations._meta.get_fields(concrete=True)
        fields = [field for field in fuelStations._meta.fields if not field.is_relation]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "products":
        context['table_data'] = product_list
        print("product_list: ", product_list)

        if data_id > 0:
            entity = products.objects.get(pk=data_id)

        print('len(products._meta.get_fields()): ', len(products._meta.get_fields()))

        # fields = products._meta.get_fields(concrete=True)
        fields = [field for field in products._meta.fields]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "reviews":
        context['table_data'] = review_list
        print("review_list: ", review_list)

        if data_id > 0:
            entity = reviews.objects.get(pk=data_id)
        print('len(reviews._meta.get_fields()): ', len(reviews._meta.get_fields()))

        # fields = reviews._meta.get_fields(concrete=True)
        fields = [field for field in reviews._meta.fields]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "cart":
        context['table_data'] = cart_list
        print("cart_list: ", cart_list)

        if data_id > 0:
            entity = cart.objects.get(pk=data_id)
        print('len(cart._meta.get_fields()): ', len(cart._meta.get_fields()))

        # fields = cart._meta.get_fields(concrete=True)
        fields = [field for field in cart._meta.fields]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "jobs":
        context['table_data'] = job_list
        print("job_list: ", job_list)

        if data_id > 0:
            entity = jobs.objects.get(pk=data_id)
        print('len(jobs._meta.get_fields()): ', len(jobs._meta.get_fields()))

        # fields = jobs._meta.get_fields(concrete=True)
        fields = [field for field in jobs._meta.fields]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "users":
        context['table_data'] = users_list
        print("users_list: ", users_list)

        if data_id > 0:
            entity = users.objects.get(pk=data_id)
        print('len(users._meta.get_fields()): ', len(users._meta.get_fields()))

        # fields = users._meta.get_fields(concrete=True)
        fields = [field for field in users._meta.fields if not field.is_relation]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "applicant":
        context['table_data'] = applicant_list
        print("applicant_list: ", applicant_list)

        if data_id > 0:
            entity = applicant.objects.get(pk=data_id)
        print('len(applicant._meta.get_fields()): ', len(applicant._meta.get_fields()))

        # fields = applicant._meta.get_fields(concrete=True)
        fields = [field for field in applicant._meta.fields]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "myadmin":
        context['table_data'] = myAdmin_list
        print("myAdmin_list: ", myAdmin_list)

        if data_id > 0:
            entity = myAdmin.objects.get(pk=data_id)
        print('len(myAdmin._meta.get_fields()): ', len(myAdmin._meta.get_fields()))

        # fields = myAdmin._meta.get_fields(concrete=True)
        fields = [field for field in myAdmin._meta.fields if not field.is_relation]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    if table_name == "order":
        context['table_data'] = order_list
        print("order_list: ", order_list)

        if data_id > 0:
            entity = order.objects.get(pk=data_id)
            
        print('len(order._meta.get_fields()): ', len(order._meta.get_fields()))

        # fields = order._meta.get_fields(concrete=True)
        fields = [field for field in order._meta.fields]

        field_names = [field.name for field in fields]

        for n in field_names:
            print("type(n): ", type(n))

        print("type(field_names): ", type(field_names))

        field_names = [x for x in field_names if x != "orderDate"]

        field_names.pop(0)

        context['field_names'] = field_names

        print("field_names: ", field_names)

    

    if request.method == 'POST':
        if action == "add":
            print("Adding")

            if table_name == "fuelstations":
                stnName = request.POST['name']
                addrs = request.POST['address']
                email = request.POST['email']
                phoneNo = request.POST['phone']
                password = request.POST['password']

                # print(stnName, addrs, email, phoneNo, password)

                Cstation_list = fuelStations.objects.all()

                query = True

                for station in Cstation_list:
                    if station.email == email:
                        print("This particular station already exists. Please Enter valid details")
                        query = False

                if query:
                    db_add = fuelStations()

                    db_add.name = stnName
                    db_add.address = addrs
                    db_add.email = email
                    db_add.phone = phoneNo
                    db_add.password = password
                    
                    db_add.save()

                    print("Admin add Fuel Station sucessfull")

            if table_name == "products":
                title = request.POST['title']
                dscrptn = request.POST['description']
                catgry = request.POST['category']
                image = request.POST['image']
                price = request.POST['price']
                details = request.POST['details']

                # print(stnName, addrs, email, phoneNo, password)

                # Cproduct_list = products.objects.all()

                query = True

                # for product in Cproduct_list:
                #     if product.title == title:
                #         print("This particular product already exists. Please Enter valid details")
                #         query = False

                if query:
                    db_add = products()

                    db_add.title = title
                    db_add.description = dscrptn
                    db_add.category = catgry
                    db_add.image = image
                    db_add.price = price
                    db_add.details = details
                    
                    db_add.save()

                    print("Admin add Product sucessfull")

            if table_name == "reviews":
                userReview = request.POST['user']
                review = request.POST['review']
                rating = request.POST['rating']

                # Creview_list = reviews.objects.all()
                first_name, last_name = userReview.split(' ')

                query = True

                # for product in Cproduct_list:
                #     if product.title == title:
                #         print("This particular product already exists. Please Enter valid details")
                #         query = False

                if query:
                    db_add = reviews()

                    db_add.user = users.objects.get(firstName=first_name, LastName=last_name)
                    db_add.review = review
                    db_add.rating = rating
                    
                    db_add.save()

                    print("Admin add Review sucessfull")

            if table_name == "cart":
                userCart = request.POST['user']

                first_name, last_name = userCart.split(' ')
                
                query = True

                if query:
                    db_add = cart()

                    db_add.user = users.objects.get(firstName=first_name, LastName=last_name)
                    
                    db_add.save()

                    print("Admin add cart sucessfull")

            if table_name == "jobs":
                job_name = request.POST['job_name']
                designation = request.POST['designation']
                Station = request.POST['fuelStation']
                details = request.POST['details']

                query = True

                if query:
                    db_add = jobs()

                    db_add.job_name = job_name
                    db_add.designation = designation
                    db_add.fuelStation = fuelStations.objects.get(name=Station)
                    db_add.details = details
                    
                    db_add.save()

                    print("Admin add job sucessfull")

            if table_name == "users":
                firstName = request.POST['firstName']
                LastName = request.POST['LastName']
                email = request.POST['email']
                phoneNo = request.POST['phone']

                # print(stnName, addrs, email, phoneNo, password)

                Cuser_list = users.objects.all()

                query = True

                for user in Cuser_list:
                    if user.email == email:
                        print("This particular user already exists. Please Enter valid details")
                        query = False

                if query:
                    db_add = users()

                    db_add.firstName = firstName
                    db_add.LastName = LastName
                    db_add.email = email
                    db_add.phone = phoneNo
                    
                    db_add.save()

                    print("Admin add Fuel Station sucessfull")

            if table_name == "applicant":
                job = request.POST['job']
                aplcnt = request.POST['user']
                cv = request.POST['cv']

                print("====================")
                print("job => ", job)
                print("aplcnt => ", aplcnt)
                print("cv => ", cv)

                first_name, last_name = aplcnt.split(' ')
                
                print("first_name => ", first_name)
                print("last_name => ", last_name)

                query = True
                print("--------------------")

                job_obj = jobs.objects.get(job_name=job)
                usr_obj = users.objects.get(firstName=first_name, LastName=last_name)

                print("job_obj => ", job_obj)
                print("usr_obj => ", usr_obj)
                print("====================")

                if query:
                    db_add = applicant()

                    db_add.job = job_obj
                    db_add.user = usr_obj
                    db_add.cv = cv
                    
                    db_add.save()

                    print("Admin add Applicant sucessfull")

            if table_name == "myadmin":
                email = request.POST['email']
                password = request.POST['password']

                # print(stnName, addrs, email, phoneNo, password)

                CmyAdmin_list = myAdmin.objects.all()

                query = True

                for admin in CmyAdmin_list:
                    if admin.email == email:
                        print("This particular admin already exists. Please Enter valid details")
                        query = False

                if query:
                    db_add = myAdmin()

                    db_add.email = email
                    db_add.password = password
                    
                    db_add.save()

                    print("Admin add Admin sucessfull")
    
            if table_name == "order":
                totalCost = request.POST['totalCost']
                Customer = request.POST['Customer']
                fuelStation = request.POST['fuelStation']

                # Corder_list = order.objects.all()

                first_name, last_name = Customer.split(' ')

                query = True

                # for order in Corder_list:
                #     if user.email == email:
                #         print("This particular user already exists. Please Enter valid details")
                #         query = False

                if query:
                    db_add = order()

                    db_add.totalCost = totalCost
                    db_add.Customer = users.objects.get(firstName=first_name, LastName=last_name)
                    db_add.fuelStation = fuelStations.objects.get(name=fuelStation)
                    
                    db_add.save()

                    print("Admin add Order sucessfull")

            # URL = '/app/myAdmin/' + table_name + '/'
            # return HttpResponseRedirect(URL, context)
            
        if action == "update":
            print("Updating")
            
            if table_name == "fuelstations":
                stnName = request.POST['name']
                addrs = request.POST['address']
                email = request.POST['email']
                phoneNo = request.POST['phone']
                password = request.POST['password']

                # print(stnName, addrs, email, phoneNo, password)

                station = fuelStations.objects.get(pk=data_id)

                station.name = stnName
                station.address = addrs
                station.email = email
                station.phone = phoneNo
                station.password = password
                
                station.save()

                print("Admin update Fuel Station sucessfull")

            if table_name == "products":
                title = request.POST['title']
                dscrptn = request.POST['description']
                catgry = request.POST['category']
                image = request.POST['image']
                price = request.POST['price']
                details = request.POST['details']

                product = products.objects.get(pk=data_id)

                product.title = title
                product.description = dscrptn
                product.category = catgry

                if image != "":
                    product.image = "images/"+image

                product.price = price
                product.details = details
                
                product.save()

                print("Admin update Product sucessfull")

            if table_name == "users":
                firstName = request.POST['firstName']
                LastName = request.POST['LastName']
                email = request.POST['email']
                phoneNo = request.POST['phone']

                user = users.objects.get(pk=data_id)

                user.firstName = firstName
                user.LastName = LastName
                user.email = email
                user.phone = phoneNo
                
                user.save()

                print("Admin add Fuel Station sucessfull")

            if table_name == "applicant":
                job = request.POST['job']
                user = request.POST['user']
                cv = request.POST['cv']

                print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
                print("job -> ", job)
                print("user -> ", user)
                print("cv -> ", cv)
                # if cv == "":
                #     print("fahfjkah fk")
                print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")

                first_name, last_name = user.split(' ')
                aplcnt = applicant.objects.get(pk=data_id)

                aplcnt.job = jobs.objects.get(job_name=job)
                aplcnt.user = users.objects.get(firstName=first_name, LastName=last_name)
                
                if cv != "":
                    aplcnt.cv = cv
                
                aplcnt.save()

                print("Admin update Applicant sucessfull")

            if table_name == "cart":
                userCart = request.POST['user']

                first_name, last_name = userCart.split(' ')

                # print(stnName, addrs, email, phoneNo, password)

                crt = cart.objects.get(pk=data_id)

                crt.user = users.objects.get(firstName=first_name, LastName=last_name)
                
                crt.save()

                print("Admin update Cart sucessfull")

            if table_name == "jobs":
                job_name = request.POST['job_name']
                designation = request.POST['designation']
                Station = request.POST['fuelStation']
                details = request.POST['details']

                # print(stnName, addrs, email, phoneNo, password)

                jb = jobs.objects.get(pk=data_id)

                jb.job_name = job_name
                jb.designation = designation
                jb.fuelStation = fuelStations.objects.get(name=Station)
                jb.details = details
                
                jb.save()

                print("Admin update Jobs sucessfull")

            if table_name == "myadmin":
                email = request.POST['email']
                password = request.POST['password']

                admin = myAdmin.objects.get(pk=data_id)

                admin.email = email
                admin.password = password
                
                admin.save()

                print("Admin update Admin sucessfull")

            if table_name == "reviews":
                userReview = request.POST['user']
                review = request.POST['review']
                rating = request.POST['rating']

                reviewUp = reviews.objects.get(pk=data_id)
                
                first_name, last_name = userReview.split(' ')

                reviewUp.user = users.objects.get(firstName=first_name, LastName=last_name)
                reviewUp.review = review
                reviewUp.rating = rating
                
                reviewUp.save()

                print("Admin update Reviews sucessfull")

            if table_name == "orders":
                totalCost = request.POST['totalCost']
                Customer = request.POST['Customer']
                fuelStation = request.POST['fuelStation']

                first_name, last_name = Customer.split(' ')

                ordr = order.objects.get(pk=data_id)

                ordr.totalCost = totalCost
                ordr.Customer = users.objects.get(firstName=first_name, LastName=last_name)
                ordr.fuelStation = fuelStations.objects.get(name=fuelStation)
                
                station.save()

                print("Admin update Order sucessfull")

        if action == "delete":
            print("Deleting")

            if table_name == "fuelstations":
                fuelStations.objects.filter(id=data_id).delete()
            
            if table_name == "products":
                products.objects.filter(id=data_id).delete()
            
            if table_name == "reviews":
                reviews.objects.filter(id=data_id).delete()
            
            if table_name == "cart":
                cart.objects.filter(id=data_id).delete()
            
            if table_name == "applicant":
                applicant.objects.filter(id=data_id).delete()
            
            if table_name == "users":
                users.objects.filter(id=data_id).delete()
            
            if table_name == "jobs":
                jobs.objects.filter(id=data_id).delete()
            
            if table_name == "myadmin":
                myAdmin.objects.filter(id=data_id).delete()
        
        return AdminSiteDetails(request, table_name)


    if data_id > 0:
        entity = model_to_dict(entity)
        
        context['entity'] = entity

        print()
        print()
        print('entity: ', entity)
        print('type(entity): ', type(entity))
        # print('len(fuelStations._meta.get_fields()): ', len(entity._meta.get_fields()))

        print("________")
        for n in field_names:
            # print(entity[n])
            if n == "Customer":
                print(n, ": ", getUserName(entity[n]))
                entityDataList.append(getUserName(entity[n]))
            elif n == "user":
                print(n, ": ", getUserName(entity[n]))
                entityDataList.append(getUserName(entity[n]))
            elif n == "fuelStation":
                print(n, ": ", getFuelStationName(entity[n]))
                entityDataList.append(getFuelStationName(entity[n]))
            elif n == "job":
                print(n, ": ", getJobName(entity[n]))
                entityDataList.append(getJobName(entity[n]))
            else:
                print(n, ": ", entity[n])
                entityDataList.append(entity[n])
 
        # entityDataList = list(entity.values())
        context['entityDataList'] = entityDataList

        num_list = [i for i in range(len(field_names))]
        context['num_list'] = num_list

        print("________")
        print()
        print()

    context['fieldLength'] = len(field_names)

    return render(request, 'adminTableAction.html', context)
