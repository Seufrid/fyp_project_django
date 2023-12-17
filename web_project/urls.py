from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("heartify.urls")),
    path('admin/', admin.site.urls),
]

handler404 = 'heartify.views.custom_404'