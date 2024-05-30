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
    path('create_service/', views.create_service, name='create_service'),
    path('update_service/', views.update_service, name='update_service'),
    path('my_services/', views.my_services, name='my_services'),
    path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
]