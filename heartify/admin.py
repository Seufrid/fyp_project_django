from django.contrib import admin
from .models import Appointment, Doctor, Contact

# Register the Doctor model with the admin site
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name of the doctor in the admin list view

# Register the Appointment model with the admin site
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'doctor', 'date', 'time', 'problem_description')  # Display these fields in the admin list view
    list_filter = ('doctor', 'date')  # Add filters for doctor and date in the admin list view
    search_fields = ('name', 'email', 'doctor__name')  # Enable search by name, email, and doctor's name in the admin list view

# Register the Contact model with the admin site
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')  # Display these fields in the admin list view
    search_fields = ('name', 'email', 'subject')  # Enable search by name, email, and subject in the admin list view
