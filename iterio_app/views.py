from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ServiceForm
from django import forms
from .models import Profile, ServiceProvider, SubCategory, Category, City


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
            return redirect('update_user')
        else:
            messages.success(request, ("Please try again..."))
            return redirect('register')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'iterio_app/register.html', context)

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'iterio_app/profile.html', {'profile': profile, 'user': request.user})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_profile = Profile.objects.get(user=current_user)

        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=current_user)
            user_info_form = UserInfoForm(request.POST, request.FILES, instance=current_profile)

            if user_form.is_valid() and user_info_form.is_valid():
                user_form.save()
                user_info_form.save()

                # Check if user type has changed
                user_type = user_info_form.cleaned_data['user_type']
                if user_type == 'provider' and not ServiceProvider.objects.filter(user=current_user).exists():
                    ServiceProvider.objects.create(user=current_user)
                elif user_type == 'regular' and ServiceProvider.objects.filter(user=current_user).exists():
                    ServiceProvider.objects.filter(user=current_user).delete()

                login(request, current_user)
                return redirect('home')
        else:
            user_form = UpdateUserForm(instance=current_user)
            user_info_form = UserInfoForm(instance=current_profile)

        context = {
            'user_form': user_form,
            'user_info_form': user_info_form,
        }
        return render(request, 'iterio_app/update_user.html', context)

    else:
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request, current_user)
                return redirect('profile')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'iterio_app/update_password.html', {'form':form})


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).all()
    return render(request, 'iterio_app/subcategory_dropdown_list_options.html', {'subcategories': subcategories})

def create_service(request):
    categories = Category.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            form.save_m2m()
            return redirect('profile')
    else:
        form = ServiceForm()

    context = {
        'form': form,
        'categories': categories,
        'cities': cities,
    }
    return render(request, 'iterio_app/create_service.html', context)

def home_services(request):
    return render(request, 'iterio_app/home_services.html')

def automotive_services(request):
    return render(request, 'iterio_app/automotive_services.html')

def health_wellness(request):
    return render(request, 'iterio_app/health_wellness.html')

def beauty_grooming(request):
    return render(request, 'iterio_app/beauty_grooming.html')

def cleaning_services(request):
    return render(request, 'iterio_app/cleaning_services.html')

def event_services(request):
    return render(request, 'iterio_app/event_services.html')

def technology_services(request):
    return render(request, 'iterio_app/technology_services.html')

def pet_services(request):
    return render(request, 'iterio_app/pet_services.html')

def education_tutoring(request):
    return render(request, 'iterio_app/education_tutoring.html')

def fitness_sport(request):
    return render(request, 'iterio_app/fitness_sport.html')

def other(request):
    return render(request, 'iterio_app/other.html')
