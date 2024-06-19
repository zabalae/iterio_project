from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ServiceForm, ServiceSlotForm, BookingForm
from django import forms
from .models import Profile, ServiceProvider, SubCategory, Category, City, Service, ServiceSlot, Booking
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.


def home(request):
    category_data = Category.objects.all()
    content = {
        'categories': category_data
    }
    return render(request, 'iterio_app/home.html', content)

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
    user = request.user
    service_provider = ServiceProvider.objects.get(user=user)
    categories = Category.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            form.save_m2m()
            service_provider.services.add(service)
            return redirect('profile')
    else:
        form = ServiceForm()

    context = {
        'form': form,
        'categories': categories,
        'cities': cities,
    }
    return render(request, 'iterio_app/create_service.html', context)


def my_services(request):
    user = request.user
    service_provider = ServiceProvider.objects.get(user=user)
    services = service_provider.services.all()
    return render(request, 'iterio_app/my_services.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'iterio_app/service_detail.html', {'service': service})


def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    subcategories = SubCategory.objects.filter(category=service.category)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('my_services')
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
        'categories': Category.objects.all(),
        'subcategories': subcategories,
        'cities': City.objects.all()
    }
    return render(request, 'iterio_app/update_service.html', context)


def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('my_services')

    context = {
        'service': service,
    }
    return render(request, 'iterio_app/delete_service.html', context)

def subcategory_selection(request, category):
    # Get all categories for the navbar
    categories = Category.objects.all()

    # Get the selected category_id from the GET parameters
    category_id = request.GET.get('category')

    # Initialize subcategories and desired_category
    subcategories = SubCategory.objects.none()
    desired_category = None

    if category_id:
        try:
            category_id = int(category_id)
            desired_category = get_object_or_404(Category, id=category_id)
            subcategories = SubCategory.objects.filter(category=desired_category)
        except (ValueError, Category.DoesNotExist):
            pass

    context = {
        'categories': categories,
        'subcategories': subcategories,
        'desired_category': desired_category,
    }
    return render(request, 'iterio_app/subcategory_selection.html', context)

def available_services(request, desired_category, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    services = subcategory.services.all()

    # Search function
    query = request.GET.get('q')
    if query:
        services = services.filter(cities__name__icontains=query).distinct()

    # Pagination logic
    paginator = Paginator(services, 5) # Show 5 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'services': services,
        'subcategory': subcategory,
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'iterio_app/available_services.html', context)

def service_slots(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    slots = ServiceSlot.objects.filter(service=service, is_booked=False).order_by('date', 'start_time')
    slots_data = [{
        'id': slot.id,
        'date': slot.date,
        'start_time': slot.start_time,
        'end_time': slot.end_time
    } for slot in slots]
    return JsonResponse(slots_data, safe=False)

@login_required
def add_service_slot(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.service = service
            slot.save()
            return redirect('service_detail', service_id=service.id)  # Redirect to the service detail page or wherever appropriate
    else:
        form = ServiceSlotForm()

    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'iterio_app/add_service_slot.html', context)

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service_slot.is_booked = True
            booking.service_slot.save()
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()

    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'iterio_app/book_service.html', context)

def booking_success(request):
    return render(request, 'iterio_app/booking_success.html')
