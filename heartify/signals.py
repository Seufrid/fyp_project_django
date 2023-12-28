# heartify/signals.py
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import PersonProfile, Appointment, Contact, SelfTestResult

@receiver(post_delete, sender=Appointment)
@receiver(post_delete, sender=Contact)
@receiver(post_delete, sender=SelfTestResult)
def auto_delete_person_profile_if_empty(sender, instance, **kwargs):
    # This function is triggered after an object of the sender type is deleted.
    # Check if the person profile related to the deleted instance is empty
    person_profile = instance.person_profile
    related_appointments = person_profile.appointments.all()
    related_contacts = person_profile.contacts.all()
    related_selftest_results = person_profile.selftest_results.all()

    if not related_appointments and not related_contacts and not related_selftest_results:
        person_profile.delete() # If there are no related objects left, delete the person profile
