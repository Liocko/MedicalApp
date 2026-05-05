from django.urls import path
from .views import (
    PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView,
    DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView,
)

app_name = 'patients'

urlpatterns = [
    path('', PatientListView.as_view(), name='list'),
    path('create/', PatientCreateView.as_view(), name='create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='delete'),

    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor_delete'),
]
