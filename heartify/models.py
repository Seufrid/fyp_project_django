from django.db import models

class PersonProfile(models.Model):
    email = models.EmailField(unique=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    doctor_id = models.CharField(max_length=10, default='')
    name = models.CharField(max_length=200, default='')
    email = models.EmailField(unique=False, default='')
    age = models.IntegerField(default=0)
    specialisation = models.CharField(max_length=200, default='')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    def __str__(self):
        return self.name

class Appointment(models.Model):
    person_profile = models.ForeignKey(PersonProfile, on_delete=models.CASCADE, related_name='appointments')
    mobile = models.CharField(max_length=20)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    problem_description = models.TextField(max_length=5000)

    def __str__(self):
        return f"{self.person_profile.name} - {self.date}"

class Contact(models.Model):
    person_profile = models.ForeignKey(PersonProfile, on_delete=models.CASCADE, related_name='contacts')
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=5000)

    
    def __str__(self):
        return f"{self.person_profile.name} - {self.subject}"

class SelfTestResult(models.Model):
    person_profile = models.ForeignKey(PersonProfile, on_delete=models.CASCADE, related_name='selftest_results')
    age = models.IntegerField()
    sex = models.CharField(max_length=10)  # Male or Female
    chest_pain_type = models.CharField(max_length=20)  # ATA, NAP, ASY, TA
    resting_bp = models.IntegerField()
    cholesterol = models.IntegerField()
    fasting_bs = models.CharField(max_length=5)  # 1 or 0
    resting_ecg = models.CharField(max_length=20)  # Normal, ST, LVH
    max_hr = models.IntegerField()
    exercise_angina = models.CharField(max_length=5)  # Yes or No
    oldpeak = models.FloatField()
    st_slope = models.CharField(max_length=10)  # Up, Flat, Down
    result = models.FloatField()

    def __str__(self):
        return f"{self.person_profile.name} - Age: {self.age}, Sex: {self.sex}"

    class Meta:
        verbose_name = "SelfTest"
        verbose_name_plural = "SelfTests"