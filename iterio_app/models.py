from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#Profile
class Profile(models.Model):
    USER_CHOICES = [
        ('regular', 'Regular User'),
        ('provider', 'Service Provider'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_CHOICES, default='regular')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create user profile by default when user signs up

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


# Automate the profile
post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sub-categories'

# Service model
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name

# ServiceProvider model
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    services = models.ManyToManyField(Service, related_name='providers')

    def __str__(self):
        return self.user.username

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.service.name} with {self.provider.user.username}"