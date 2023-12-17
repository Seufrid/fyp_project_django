from django.urls import path
from heartify import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('selftest/', views.selftest, name='selftest'),
    path('appointment/', views.appointment, name='appointment'),
]

urlpatterns += staticfiles_urlpatterns()