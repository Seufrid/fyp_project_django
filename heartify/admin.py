from django.contrib import admin
from .models import Appointment, Doctor, Contact

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'doctor', 'date', 'time', 'problem_description')
    list_filter = ('doctor', 'date')
    search_fields = ('name', 'email', 'doctor__name')  # You can search by doctor's name

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    search_fields = ('name', 'email', 'subject')