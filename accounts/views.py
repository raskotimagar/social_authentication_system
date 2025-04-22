from django.shortcuts import render, redirect
from.forms import CustomLoginForm, CustomSignupForm
from django.contrib.auth import login,logout
from django.contrib import messages
from allauth.account.models import EmailAddress
from .models import CustomUser

# Create your views here.

def home_view(request):
    return render(request, 'home.html')


def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request) # Save the user
            login(request, user, backend='accounts.backends.CustomAuthBackend') # Logs in the newly created user
            return redirect('home') # Redirect to home page
    else:
        form= CustomSignupForm()

    return render(request, 'accounts/signup.html', {'form': form}) 


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user() # Retrieves an EXISTING user
            login(request, user) # Logs in the authenticated user
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home') # Redirect to home after logout

