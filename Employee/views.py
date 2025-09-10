from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import EmployeeDetails
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required


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


# @login_required(login_url='/emp_login/')
def profile(request):
    error = ""
    user = request.user

    # Get employee details for the logged-in user
    try:
        employee = EmployeeDetails.objects.get(user=user)
    except EmployeeDetails.DoesNotExist:
        employee = None

    if request.method == "POST":
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        ec = request.POST.get('empcode')
        em = request.POST.get('email')
        pwd = request.POST.get('pwd')

        try:
            # Update the logged-in user instead of creating a new one
            user.first_name = fn
            user.last_name = ln
            user.username = em
            if pwd:   # only update password if entered
                user.set_password(pwd)
            user.save()

            # Update or create employee details
            if employee:
                employee.empcode = ec
                employee.save()
            else:
                employee = EmployeeDetails.objects.create(user=user, empcode=ec)

            error = "no"
        except Exception as e:
            print("Error while updating profile:", e)
            error = "yes"

    return render(request, 'profile.html', {'employee': employee, 'user': user, 'error': error})

        


def admin_login(request):
    return render(request, 'admin_login.html')

