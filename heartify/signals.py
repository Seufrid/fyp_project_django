from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import Appointment, Contact, SelfTestResult, PersonProfile

@receiver(post_delete, sender=Appointment)
@receiver(post_delete, sender=Contact)
@receiver(post_delete, sender=SelfTestResult)
def auto_delete_person_profile_if_empty(sender, instance, **kwargs):
    try:
        person_profile = instance.person_profile
    except PersonProfile.DoesNotExist:
        # PersonProfile has already been deleted, so nothing to do here
        return

    # Proceed only if the PersonProfile exists
    related_appointments = person_profile.appointments.all()
    related_contacts = person_profile.contacts.all()
    related_selftest_results = person_profile.selftest_results.all()

    if not related_appointments and not related_contacts and not related_selftest_results:
        person_profile.delete()
