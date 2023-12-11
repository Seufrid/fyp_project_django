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
    return HttpResponse("Hello, Django!")


def about(request):
    return render(request, "web_project/about.html", data)

def contact(request):
    return render(request, "web_project/contact.html", "hello world")

def contact(request):
    return render(request, "web_project/contact.html", data)