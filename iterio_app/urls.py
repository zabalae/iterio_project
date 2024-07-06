from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.aboutUs, name='about'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('profile/', views.profile, name='profile'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<username>/', views.inbox_detail, name='inbox_detail'),
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('create-service/', views.create_service, name='create_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('my-services/', views.my_services, name='my_services'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('view_profile/<int:provider_id>/', views.view_provider_profile, name='service_provider_profile'),
    path('add_time_slot/<int:service_id>/', views.add_time_slot, name='add_time_slot'),
    path('delete_profile/', views.delete_profile, name="delete_profile"),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('<str:category>/', views.subcategory_selection, name='subcategory_selection'), # works
    path('<str:desired_category>/<int:subcategory_id>/', views.available_services, name='available_services'), # works
    path('services/<int:service_id>/book/', views.book_service_page, name='book_service_page'), # works
    path('services/<int:service_id>/time_slots/', views.time_slots_created, name='time_slots_created'),
    path('services/<int:service_id>/add_slot/', views.add_time_slot, name='add_service_slot'),
    path('services/<int:service_id>/slots/', views.service_slots, name='service_slots'),
    path('book-time-slot/<int:service_id>/', views.book_time_slot, name='book_time_slot'),
    path('timeslot/<int:timeslot_id>/update/', views.update_time_slot, name='update_time_slot'),
    path('timeslot/<int:timeslot_id>/delete/', views.delete_time_slot, name='delete_time_slot'),
]
