import json
import joblib
import datetime
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse
from .ml_utils import make_prediction
from django.core.mail import send_mail
from .models import Appointment, Doctor, Contact, SelfTestResult, PersonProfile

def home(request):
    # Render the home page
    return render(request, "heartify/home.html")

def about(request):
    # Render the about page
    return render(request, "heartify/about.html")

def contact(request):
    if request.method == 'POST':
        # Handle the contact form submission
        name = request.POST.get('name', 'No Name')
        email = request.POST.get('email', 'No Email')
        subject = request.POST.get('subject', 'No Subject')
        message = request.POST.get('message', 'No Message')

        try:
            # Get or create a PersonProfile instance
            person_profile, created = PersonProfile.objects.get_or_create(
                email=email, defaults={'name': name}
            )

            # Save the contact message in the database
            contact = Contact(person_profile=person_profile, name=name, email=email, subject=subject, message=message)
            contact.save()

            # Customize the email content and recipient
            email_content = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
            recipient_email = 'usamaabdul11@gmail.com'

            # Send email to the recipient and the user
            send_mail(
                subject='Heartify Contact Form Submission',
                message=email_content,
                from_email=email,
                recipient_list=[recipient_email, email],
                fail_silently=False,
            )

            # Return a JSON response indicating success or an error
            return JsonResponse({'status': 'success', 'message': 'Contact form submitted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to submit contact form. Please check the form and try again.', 'errors': str(e)})

    # If not a POST request, render the contact page
    return render(request, "heartify/contact.html")

def selftest(request):
    if request.method == 'POST':
        # Handle the self-test form submission
        age = int(request.POST.get('Age', 0))
        sex = int(request.POST.get('Sex', 0))
        chest_pain_type = int(request.POST.get('ChestPainType', 0))
        resting_bp = int(request.POST.get('RestingBP', 0))
        cholesterol = int(request.POST.get('Cholesterol', 0))
        fasting_bs = int(request.POST.get('FastingBS', 0))
        resting_ecg = int(request.POST.get('RestingECG', 0))
        max_hr = int(request.POST.get('MaxHR', 0))
        exercise_angina = int(request.POST.get('ExerciseAngina', 0))
        oldpeak = int(request.POST.get('Oldpeak', 0))
        st_slope = int(request.POST.get('STSlope', 0))

        # Get or create the PersonProfile instance
        person_profile, created = PersonProfile.objects.get_or_create(
            email=request.POST.get('email'), defaults={'name': request.POST.get('name')}
        )
        
        # Make prediction and return result
        result = make_prediction(age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope)

        # Converting encoded values to human-readable strings
        sex_str = "Male" if sex == 1 else "Female"
        chest_pain_type_str = {0: "ATA", 1: "NAP", 2: "ASY", 3: "TA"}.get(chest_pain_type, "Unknown")
        fasting_bs_str = "1" if fasting_bs == 1 else "0"
        resting_ecg_str = {0: "Normal", 1: "ST", 2: "LVH"}.get(resting_ecg, "Unknown")
        exercise_angina_str = "Yes" if exercise_angina == 1 else "No"
        st_slope_str = {0: "Up", 1: "Flat", 2: "Down"}.get(st_slope, "Unknown")

        # Create an instance of the SelfTestResult model
        test_result = SelfTestResult(
            person_profile=person_profile,
            age=age,
            sex=sex_str,
            chest_pain_type=chest_pain_type_str,
            resting_bp=resting_bp,
            cholesterol=cholesterol,
            fasting_bs=fasting_bs_str,
            resting_ecg=resting_ecg_str,
            max_hr=max_hr,
            exercise_angina=exercise_angina_str,
            oldpeak=oldpeak,
            st_slope=st_slope_str,
            result= round(result * 100)
        )

        # Save the instance to the database
        test_result.save()

        # Average data for positive and negative outcomes (all features included)
        avg_data_positive_outcome = {
            'Age': 55.9, 
            'Sex': 0.9,  # 0 for Female, 1 for Male
            'ChestPainType': 1.8,  # 0: ATA, 1: NAP, 2: ASY, 3: TA
            'RestingBP': 134.19,
            'Cholesterol': 175.94,
            'FastingBS': 0.33,
            'RestingECG': 0.65,  # 0: Normal, 1: ST, 2: LVH
            'MaxHR': 127.66,
            'ExerciseAngina': 0.62,  # 0: No, 1: Yes
            'Oldpeak': 1.27,
            'ST_Slope': 0.94  # 0: Up, 1: Flat, 2: Down
        }

        avg_data_negative_outcome = {
            'Age': 50.55,
            'Sex': 0.65,  # 0 for Female, 1 for Male
            'ChestPainType': 1.02,  # 0: ATA, 1: NAP, 2: ASY, 3: TA
            'RestingBP': 130.18,
            'Cholesterol': 227.12,
            'FastingBS': 0.11,
            'RestingECG': 0.55,  # 0: Normal, 1: ST, 2: LVH
            'MaxHR': 148.15,
            'ExerciseAngina': 0.13,  # 0: No, 1: Yes
            'Oldpeak': 0.41,
            'ST_Slope': 0.26  # 0: Up, 1: Flat, 2: Down
        }

        # Customize the email content and recipient
        email_content = (
            f"Date Submitted: {date.today()}\n"
            f"Time Submitted: {datetime.datetime.now().strftime('%I:%M %p')}\n\n"
            f"Heartify Selftest Form Submission\n"
            f"Name: {person_profile.name}\n"
            f"Email: {person_profile.email}\n"
            f"Age: {age}\n"
            f"Sex: {sex_str}\n"
            f"Chest Pain Type: {chest_pain_type_str}\n"
            f"Resting BP: {resting_bp}\n"
            f"Cholesterol: {cholesterol}\n"
            f"Fasting BS: {fasting_bs_str}\n"
            f"Resting ECG: {resting_ecg_str}\n"
            f"Max HR: {max_hr}\n"
            f"Exercise Angina: {exercise_angina_str}\n"
            f"Oldpeak: {oldpeak}\n"
            f"ST Slope: {st_slope_str}\n\n"
            f"Result: {round(result * 100)}%"
        )
        recipient_email = 'usamaabdul11@gmail.com'
        
        # Send email to the recipient and the user
        send_mail(
            subject='Heartify Selftest Form Submission (' + str(date.today()) + ')',
            message=email_content,
            from_email=person_profile.email,
            recipient_list=[recipient_email, person_profile.email],
            fail_silently=False,
        )

        # Load your scaler and PCA
        scaler = joblib.load(open("scaler.sav", "rb"))
        pca = joblib.load(open("pca.sav", "rb"))

        # Scale the input data
        scaled_data = scaler.transform([[age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope]])

        # Transform the data using PCA
        pca_data = pca.transform(scaled_data)
        new_point = {
            'x': pca_data[0][0],
            'y': pca_data[0][1]
        }

        # Import PCA class 1 data from JSON file
        with open('pca_data_class_0.json', 'r') as f:
            pca_data_class_0 = json.load(f)

        # Import PCA class 2 data from JSON file
        with open('pca_data_class_1.json', 'r') as f:
            pca_data_class_1 = json.load(f)

        # Import the decision boundary data from JSON file
        with open('decision_boundary.json', 'r') as f:
            decision_boundary = json.load(f)

        # Import feature importance data from JSON file
        with open('feature_importance.json', 'r') as f:
            feature_importance_data = json.load(f)

        # Return a JSON response with all the data
        return JsonResponse({
            'status': 'success',
            'message': 'Self-test form submitted successfully.',
            'result': result,
            'avg_positive': avg_data_positive_outcome,
            'avg_negative': avg_data_negative_outcome,
            'feature_importance': feature_importance_data,
            'new_point': new_point,
            'pca_class_0': pca_data_class_0,
            'pca_class_1': pca_data_class_1,
            'decision_boundary': decision_boundary
        })
    else:
        # If not a POST request, render the self-test page and return the response data
        return render(request, "heartify/selftest.html", {'response_data': {'status': 'error', 'message': 'Failed to submit self-test form. Please check the form and try again.'}})

def appointment(request):
    if request.method == 'POST':
        # Handle the appointment booking form submission
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        doctor_name = request.POST.get('doctor', '')
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')
        problem_description = request.POST.get('problem_description', '')

        try:
            # Get or create the PersonProfile instance
            person_profile, created = PersonProfile.objects.get_or_create(
                email=email, defaults={'name': name}
            )
            
            # Save the appointment in the database
            doctor = Doctor.objects.get(name=doctor_name)
            appointment = Appointment(
                person_profile=person_profile,
                mobile=mobile,
                doctor=doctor,
                date=date,
                time=time,
                problem_description=problem_description
            )
            appointment.save()

            # Customize the email content and recipient
            email_content = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Mobile: {mobile}\n"
                f"Doctor: {doctor_name}\n"
                f"Date: {date}\n"
                f"Time: {time}\n\n"
                f"{problem_description}"
            )
            recipient_email = 'usamaabdul11@gmail.com'

            # Send email to the recipient and the user
            send_mail(
                subject='Heartify Appointment Form Submission',
                message=email_content,
                from_email=email,
                recipient_list=[recipient_email, email],
                fail_silently=False,
            )

            # Return a JSON response indicating success or an error
            return JsonResponse({'status': 'success', 'message': 'Appointment booked successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to book an appointment. Please check the form and try again.', 'errors': str(e)})
    else:
        # If not a POST request, render the appointment page
        response_data = {'status': 'error', 'message': 'Invalid request method.'}
        doctor_names = Doctor.objects.all()
        return render(request, "heartify/appointment.html", {'doctor_names': doctor_names, 'response_data': response_data})
    
def custom_404(request, exception):
    # Custom 404 page
    return render(request, 'heartify/404.html', status=404)