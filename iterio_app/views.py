from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UpdateUserForm
from django import forms


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


def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
            return redirect('home')
        else:
            messages.success(request, ("Please try again..."))
            return redirect('register')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'iterio_app/register.html', context)

def profile(request):
    return render(request, 'iterio_app/profile.html')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)

            return redirect('home')
        return render(request, 'iterio_app/update_user.html', {'user_form': user_form})

    else:
        return redirect('home')