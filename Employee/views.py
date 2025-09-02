from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import EmployeeDetails
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .models import EmployeeDetails


def index(request):
    return render(request, 'index.html')

def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST.get('first_name')
        ln = request.POST.get('last_name')
        ec = request.POST.get('employee_code')
        em = request.POST.get('email')
        pwd = request.POST.get('password')   

    # try:
        user= User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd)
        EmployeeDetails.objects.create(empcode=ec,user=user)
        error="no"
    # except:
        error="yes"
    return render(request,'registration.html',locals())


def emp_login(request):
    error=""
    if request.method == "POST":
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('emp_home') 
            error ="no"
        else:
            error="yes"
    return render(request, 'emp_login.html',locals())



def emp_home(request):
    print("User:", request.user)
    print("Authenticated:", request.user.is_authenticated)
    return render(request, 'emp_home.html')


def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    # user = request.user
    # employee = EmployeeDetails.objects.get(user=user)

    employee = EmployeeDetails.objects.filter(user=request.user).first()

    if request.method == "PO[[[]":
        fn = request.POST.get('first_name')
        ln = request.POST.get('last_name')
        ec = request.POST.get('employee_code')
        dept = request.POST.get('department')
        designation = request.POST.get('designation')   
        contact = request.POST.get('contact')
        jdate = request.POST.get('jdate') 
        gender = request.POST.get('Gender')

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation =designation 
        employee.contact = contact 
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate

        

    # try:
        employee.save()
        employee.user.save()
        error ="no"
    # except:
        error="yes"
    return render(request,'profile.html',locals())


def admin_login(request):
    return render(request, 'admin_login.html')

def myexperience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    experience = EmployeeExperience.objects.get(user=user)

    return render(request,'myexperience.html',locals())