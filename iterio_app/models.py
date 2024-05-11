from django.db import models
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class ServiceProvider(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    service_type = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)
    service_description = models.CharField(max_length=100)

