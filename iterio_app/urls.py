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
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('create-service/', views.create_service, name='create_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('my-services/', views.my_services, name='my_services'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('<str:category>/', views.subcategory_selection, name='subcategory_selection'),
    path('<str:desired_category>/<int:subcategory_id>/', views.available_services, name='available_services'),
    path('services/<int:service_id>/book/', views.book_service, name='book_service'),
    path('services/<int:service_id>/add_slot/', views.add_service_slot, name='add_service_slot'),
    path('services/<int:service_id>/slots/', views.service_slots, name='service_slots'),
    path('booking_success/', views.booking_success, name='booking_success'),
]
