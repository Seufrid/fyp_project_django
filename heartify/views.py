from django.shortcuts import render
from django.http import JsonResponse
from .ml_utils import make_prediction
from django.core.mail import send_mail
from .models import Appointment, Doctor, Contact

def home(request):
    return render(request, "heartify/home.html")

def about(request):
    return render(request, "heartify/about.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        try:
            # Save the contact message in the database
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()

            # Customize the email content and recipient as needed
            email_content = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
            recipient_email = 'heartifycontact@gmail.com'

            # Send email to the recipient and the user
            send_mail(
                subject='Contact Form Submission',
                message=email_content,
                from_email=email,
                recipient_list=[recipient_email, email],
                fail_silently=False,
            )

            # Return a JSON response indicating success or an error
            return JsonResponse({'status': 'success', 'message': 'Appointment booked successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to book appointment. Please check the form and try again.', 'errors': str(e)})

    # If not a POST request, render the contact page
    return render(request, "heartify/contact.html")

def selftest(request):
    if request.method == 'POST':
        age = int(request.POST['Age'])
        sex = int(request.POST['Sex'])
        chest_pain_type = int(request.POST['ChestPainType'])
        resting_bp = int(request.POST['RestingBP'])
        cholesterol = int(request.POST['Cholesterol'])
        fasting_bs = int(request.POST['FastingBS'])
        resting_ecg = int(request.POST['RestingECG'])
        max_hr = int(request.POST['MaxHR'])
        exercise_angina = int(request.POST['ExerciseAngina'])
        oldpeak = int(request.POST['Oldpeak'])
        st_slope = int(request.POST['STSlope'])
        
        # Make prediction and return result
        result = make_prediction(age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope)

        # Return a JSON response with the prediction
        return JsonResponse({'result': result})
    else:
        # If not a POST request, render the selftest page
        return render(request, "heartify/selftest.html")

def appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        doctor_name = request.POST.get('doctor', '')
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')
        problem_description = request.POST.get('problem_description', '')

        try:
            # Save the appointment in the database
            doctor = Doctor.objects.get(name=doctor_name)
            appointment = Appointment(name=name, email=email, mobile=mobile, doctor=doctor, date=date, time=time, problem_description=problem_description)
            appointment.save()

            # Customize the email content and recipient as needed
            email_content = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Mobile: {mobile}\n"
                f"Doctor: {doctor_name}\n"
                f"Date: {date}\n"
                f"Time: {time}\n\n"
                f"{problem_description}"
            )
            recipient_email = 'heartifycontact@gmail.com'

            # Send email to the recipient and the user
            send_mail(
                subject='Appointment Form Submission',
                message=email_content,
                from_email=email,
                recipient_list=[recipient_email, email],
                fail_silently=False,
            )

            # Return a JSON response indicating success or an error
            return JsonResponse({'status': 'success', 'message': 'Appointment booked successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to book appointment. Please check the form and try again.', 'errors': str(e)})
    else:
        # If not a POST request, render the appointment page
        response_data = {'status': 'error', 'message': 'Invalid request method.'}
        doctor_names = Doctor.objects.all()
        return render(request, "heartify/appointment.html", {'doctor_names': doctor_names, 'response_data': response_data})