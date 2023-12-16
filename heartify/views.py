from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from django.http import HttpResponse
import pickle
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail

# def home(request):
#     return HttpResponse("Hello, Django!")

def hello(request):
    return render(request,'heartify/hello_there.html')

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

        # Customize the email content and recipient as needed
        email_content = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
        recipient_email = 'usamaabdul11@gmail.com'

        send_mail(
            subject='Contact Form Submission',
            message=email_content,
            from_email=email,
            recipient_list=[recipient_email, email],
            fail_silently=False,
        )

        # Return a JSON response indicating success
        response_data = {'success': True}
        return JsonResponse(response_data)

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

        model = pickle.load(open("heart_model.sav", "rb"))
        prediction = model.predict_proba([[age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope]])
        result = prediction[0][1]

        return JsonResponse({'result': result})
    else:
        return render(request, "heartify/selftest.html")
    
def appointment(request):
    return render(request, "heartify/appointment.html")
    
# def appointment(request):
#     if request.method == 'POST':
#         # Retrieve form data from the request
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         mobile = request.POST.get('mobile')
#         doctor = request.POST.get('doctor')
#         date = request.POST.get('date')
#         time = request.POST.get('time')
#         problem_description = request.POST.get('problem_description')

#         # Create an Appointment instance and save it to the database
#         appointment = Appointment(
#             name=name,
#             email=email,
#             mobile=mobile,
#             doctor=doctor,
#             date=date,
#             time=time,
#             problem_description=problem_description
#         )
#         appointment.save()

#         return redirect('appointment.html')  # Redirect to a success page or URL

#     return render(request, 'appointment.html')
    
# def appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             response_data = {'status': 'success', 'message': 'Appointment booked successfully!'}
#         else:
#             response_data = {'status': 'error', 'errors': form.errors}
        
#         # Check for AJAX request using headers
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             return JsonResponse(response_data)
#     else:
#         form = AppointmentForm()

#     return render(request, 'appointment.html', {'form': form})

def test(request):
    return render(request, "heartify/test.html")