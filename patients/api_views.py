from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Patient, Doctor
from .serializers import PatientSerializer, DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('last_name', 'first_name')
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['last_name', 'first_name', 'date_of_birth', 'created_at']


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('last_name', 'first_name')
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'specialization', 'email']
    ordering_fields = ['last_name', 'first_name', 'specialization']
