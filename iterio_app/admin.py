from django.contrib import admin
from .models import Category, Profile, SubCategory, Service, ServiceProvider, Booking, City, TimeSlot, ChatMessage
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Profile)


# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['message']
    list_display = ['sender', 'receiver', 'message', 'is_read']

admin.site.unregister(User)

admin.site.register(User, UserAdmin)

admin.site.register(Service)
admin.site.register(ServiceProvider)
admin.site.register(Booking)
admin.site.register(SubCategory)
admin.site.register(City)
admin.site.register(TimeSlot)
admin.site.register(ChatMessage, ChatMessageAdmin)
