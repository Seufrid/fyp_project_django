import pickle
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

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
    return render(request, "contact.html")

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
        return render(request, "selftest.html")
    
def appointment(request):
    return render(request, "appointment.html")

def test(request):
    return render(request, "test.html")