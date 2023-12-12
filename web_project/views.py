from django.http import HttpResponse
from django.shortcuts import render

data = {
    "reasons_to_learn": [
        {"reason": "Clean design"},
        {"reason": "Python power"},
        {"reason": "Community"},
        {"reason": "Django is fun"},
        {"reason": "Job market"},
    ],
}


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def selftest(request):
    return render(request, "selftest.html")

def appointment(request):
    return render(request, "appointment.html")