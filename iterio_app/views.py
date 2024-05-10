from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'iterio_app/home.html')

def aboutUs(request):
    return render(request, 'iterio_app/aboutUs.html')

def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'iterio_app/loginPage.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')