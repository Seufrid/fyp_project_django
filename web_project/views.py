from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello, Django!")

def about(request):
    return render(request, "web_project/about.html", {'about': ['About', 'about2']})