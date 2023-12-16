import pickle
from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
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
