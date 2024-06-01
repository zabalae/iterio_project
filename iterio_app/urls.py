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
    path('home_services/', views.home_services, name='home_services'),
    path('automotive_services/', views.automotive_services, name='automotive_services'),
    path('health_wellness/', views.health_wellness, name='health_wellness'),
    path('beauty_grooming/', views.beauty_grooming, name='beauty_grooming'),
    path('cleaning_services/', views.cleaning_services, name='cleaning_services'),
    path('event_services/', views.event_services, name='event_services'),
    path('technology_services/', views.technology_services, name='technology_services'),
    path('pet_services/', views.pet_services, name='pet_services'),
    path('education_tutoring/', views.education_tutoring, name='education_tutoring'),
    path('fitness_sport/', views.fitness_sport, name='fitness_sport'),
    path('other/', views.other, name='other')
]
