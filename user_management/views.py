from django.shortcuts import render, redirect
from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def signin(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, emp_id=employee_id, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')  # Replace 'dashboard' with your dashboard URL name
            else:
                form.add_error(None, "Invalid credentials. Please try again.")

    else:
        form = LoginForm()
    return render(request,  'registration/login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                emp_id=form.cleaned_data['employee_id'],
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            group = Group.objects.get(name='EMPLOYEE')
            group.user_set.add(user)
            messages.success(request, 'Account created successfully.')
            return redirect('/')
    else:
        form = SignupForm()

    return render(request,'registration/register.html', {'form': form})


def userlogout(request):
    logout(request)
    return redirect('/')

@login_required
def dashboard(request):

  
    return render(request,'index.html')