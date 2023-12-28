from django.db import models
from django.contrib import admin
from django.forms import Textarea
from .models import Appointment, Doctor, Contact, SelfTestResult, PersonProfile

# Register the Doctor model with the admin site
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor_id', 'specialisation')  # Display these fields in the admin list view

# Register the Appointment model with the admin site
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'date', 'time', 'problem_description')

    def get_name(self, obj):
        return obj.person_profile.name
    get_name.admin_order_field = 'person_profile__name'  # Allows column order sorting
    get_name.short_description = 'Name'  # Renames column head

    def get_email(self, obj):
        return obj.person_profile.email
    get_email.admin_order_field = 'person_profile__email' 
    get_email.short_description = 'Email'  

# Register the Contact model with the admin site
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'subject')

    def get_name(self, obj):
        return obj.person_profile.name
    get_name.admin_order_field = 'person_profile__name'
    get_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.person_profile.email
    get_email.admin_order_field = 'person_profile__email'
    get_email.short_description = 'Email'

# Register the SelfTestResult model with the admin site
@admin.register(SelfTestResult)
class SelfTestResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SelfTestResult._meta.get_fields()]

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 17})},  
    }

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 8, 'cols': 20})},  
    }

class SelfTestResultInline(admin.TabularInline):
    model = SelfTestResult
    fields = ('age', 'sex', 'chest_pain_type', 'resting_bp', 'cholesterol', 'result')
    extra = 0

@admin.register(PersonProfile)
class PersonProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    inlines = [AppointmentInline, ContactInline, SelfTestResultInline]