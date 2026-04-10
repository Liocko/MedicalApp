from django.urls import path
from .views import patient_list

urlpatterns = [
    path("", patient_list, name="patient_list"),
]
