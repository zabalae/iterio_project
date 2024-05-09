from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'iterio_app/home.html')

def aboutUs(request):
    return render(request, 'iterio_app/aboutUs.html')