from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ServiceForm, TimeSlotForm, BookingForm, DeleteProfileForm
from django import forms
from .models import Profile, ServiceProvider, SubCategory, Category, City, Service, TimeSlot, Booking
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
import asyncio
from mailer import connection
import datetime
from django.views.decorators.http import require_POST

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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'iterio_app/loginPage.html', {'form': form})

def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def registerUser(request):
    users = User.objects.all()
    form = SignUpForm(request.POST)
    all_emails = []
    context = {'form': form}
    for user in users:
        all_emails.append(user.email)
    if request.method == 'POST':
        if form.is_valid() and form.cleaned_data['email'] not in all_emails:
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user_email = form.cleaned_data['email']
            #asyncio.run(connection.welcome_msg(username, user_email))
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
            return redirect('update_user')
        else:
            if not form.cleaned_data['username']:
                context["invalid_username"] = True
            if form.cleaned_data['email'] in all_emails:
                context['invalid_email'] = True
            messages.success(request, ("Please try again..."))
            return render(request, 'iterio_app/register.html', context)
    else:
        form = SignUpForm()
    all_emails = []
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
                return redirect('profile')
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

@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        form = DeleteProfileForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if user.check_password(password):
                print("#" * 55)
                try:
                    service_provider = ServiceProvider.objects.get(user=user)
                    services = service_provider.services.all()
                    for service in services:
                        print(f"#\tDeleted Service --> {str(service)}")
                        service.delete()
                except:
                    print("#\n#\n#\t---> No Services found To Delete <---\n#\n#")
                print(f"#\tDELETED PROFILE:\n#\t\t{str(user.username)}")
                print("#" * 55)
                user.delete()
                messages.success(request, 'Your profile has been deleted.')
                return redirect('home')
            else:
                return render(request, 'iterio_app/delete_profile.html', {'form': form, 'Incorrect': True})
    else:
        form = DeleteProfileForm()
    return render(request, 'iterio_app/delete_profile.html', {'form': form})


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


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    time_slots = TimeSlot.objects.filter(service=service, is_booked=False)

    context = {
        'service': service,
        'time_slots': time_slots,
    }
    return render(request, 'iterio_app/service_detail.html', context)


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
    paginator = Paginator(services, 3) # Show 5 services per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'services': services,
        'subcategory': subcategory,
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'iterio_app/available_services.html', context)

# This is for time slots in calendar view in book_service.html
def service_slots(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    timeslots = TimeSlot.objects.filter(service=service)
    events = []
    for timeslot in timeslots:
        start_datetime = datetime.datetime.combine(timeslot.date, timeslot.start_time)
        end_datetime = datetime.datetime.combine(timeslot.date, timeslot.end_time)
        events.append({
            "title": f"{ service.name }",
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
        })
    return JsonResponse(events, safe=False)

# This is to create time slots
@login_required
def add_time_slot(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.service = service
            slot.save()
            return redirect('time_slots_created', service_id=service.id)  # Redirect to the service detail page or wherever appropriate
    else:
        form = TimeSlotForm()

    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'iterio_app/add_time_slot.html', context)

# This is for the service provider to be able to view the time slots he/she created
@login_required
def time_slots_created(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    timeslots = TimeSlot.objects.filter(service=service)

    context = {
        'service': service,
        'timeslots': timeslots,
    }
    return render(request, 'iterio_app/time_slots_created.html', context)

# This is for the provider to be able to update the time slot
@login_required
def update_time_slot(request, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
    if request.method == 'POST':
        form = TimeSlotForm(request.POST, instance=timeslot)
        if form.is_valid():
            form.save()
            return redirect('time_slots_created', service_id=timeslot.service.id)
    else:
        form = TimeSlotForm(instance=timeslot)

    context = {
        'form': form,
        'timeslot': timeslot
    }
    return render(request, 'iterio_app/update_time_slot.html', context)

# This allows the provider to delete a timeslot
@login_required
def delete_time_slot(request, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
    service_id = timeslot.service.id
    timeslot.delete()
    return redirect('time_slots_created', service_id=service_id)

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

# This is for the user to book the time slot selected
@require_POST
@login_required
def book_timeslot(request, service_id):
    timeslot_id = request.POST.get('timeslot_id')
    try:
        timeslot = TimeSlot.objects.get(id=timeslot_id, service_id=service_id)
        
        # Check if the timeslot is already booked
        if timeslot.is_booked:
            return JsonResponse({'error': 'Timeslot already booked.'}, status=400)

        # Create a new booking
        booking = Booking.objects.create(user=request.user, service_slot=timeslot)
        timeslot.is_booked = True
        timeslot.save()
        
        return JsonResponse({'message': 'Timeslot booked successfully.'})
    
    except TimeSlot.DoesNotExist:
        return JsonResponse({'error': 'Invalid timeslot.'}, status=400)

def booking_success(request):
    return render(request, 'iterio_app/booking_success.html')

# This allows the users to see the bookings they have made
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)

    context = {
        'bookings': bookings
    }
    return render(request, 'iterio_app/my_bookings.html', context)


def view_provider_profile(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    profile = provider.user.profile  # Access the Profile through the User
    context = {
        'provider': provider,
        'profile': profile,
    }
    return render(request, 'iterio_app/view_provider_profile.html', context)
