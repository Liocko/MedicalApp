from django.urls import path
from .views import record_list

urlpatterns = [
    path("", record_list, name="record_list"),
]
