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
    error = ""
    if request.method == "POST":
        email = request.POST.get('emailid')
        password = request.POST.get('password')

        print("Login attempt:", email, password)  # Debug print

        try:
            # Try to find user by username first
            user_obj = User.objects.get(username=email)
        except User.DoesNotExist:
            # If username is not email, try to find by email field
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                user_obj = None

        if user_obj:
            user = authenticate(username=user_obj.username, password=password)
            if user:
                login(request, user)
                print("Login successful for:", user.username)
                return redirect('emp_home')
            else:
                print("Authentication failed: wrong password")
                error = "yes"
        else:
            print("No user found with this email/username")
            error = "yes"

    return render(request, 'emp_login.html', {'error': error})

def emp_home(request):
    # if not request.user.is_authenticated:
    #     return redirect ('emp_login')
    return render (request,'emp_home.html')


def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    error = ""
    employee = None
    user = request.user

    # Check if user is authenticated
    if user.is_authenticated:
        # Safely get employee record, if it exists
        employee = EmployeeDetails.objects.filter(user=user).first()

    if request.method == "POST" and employee:
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        ec = request.POST.get('empcode')
        em = request.POST.get('department')
        designation = request.POST.get('designation')
        contact = request.POST.get('contact')
        jdate = request.POST.get('jdate')
        gender = request.POST.get('gender')

        # Update fields
        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = em
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate

        try:
            employee.user.save()
            employee.save()
            error = "no"
        except Exception as e:
            print("Error saving profile:", e)
            error = "yes"

    # Render profile page, pass employee (could be None for anonymous users)
    return render(request, 'profile.html', {'employee': employee, 'error': error})

        


    
def admin_login(request):
    return render(request, 'admin_login.html')


# def my_experience(request):
#     if not request.user.is_authenticated:
#         return redirect ('emp_login')
    
#     error =""
#     user = request.user
#     experience = EmployeeDetails.objects.get(user = user)

#     return render (request,'my_experience.html',locals())

def my_experience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    
    error = ""
    user = request.user
    
    # Use filter().first() to avoid DoesNotExist
    experience1 = EmployeeDetails.objects.filter(user=user)

    if not experience1:
        error = "no_experience"  # you can use this in template to show a message

    return render(request, 'my_experience.html', {'experience': experience1, 'error': error})


def edit_experience(request):
    error = ""
    employee = None
    user = request.user

    # Check if user is authenticated
    if user.is_authenticated:
        # Safely get employee record, if it exists
        experience = EmployeeExperience.objects.filter(user=user).first()

    if request.method == "POST" and employee:
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        ec = request.POST.get('empcode')
        em = request.POST.get('department')
        designation = request.POST.get('designation')
        contact = request.POST.get('contact')
        jdate = request.POST.get('jdate')
        gender = request.POST.get('gender')

        # Update fields
        experience.user.first_name = fn
        experience.user.last_name = ln
        experience.empcode = ec
        experience.empdept = em
        experience.designation = designation
        experience.contact = contact
        experience.gender = gender



        try:
            experience.user.save()
            error = "no"
        except Exception as e:
            print("Error saving profile:", e)
            error = "yes"

    # Render profile page, pass employee (could be None for anonymous users)
    return render(request, 'edit_experience.html', {'employee': employee, 'error': error})

        


    
