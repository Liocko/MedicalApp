from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord, Report
from .serializers import MedicalRecordSerializer, ReportSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related('patient', 'doctor').order_by('-created_at')
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'diagnosis', 'patient__last_name', 'patient__first_name']
    ordering_fields = ['created_at', 'updated_at', 'title']


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related('patient', 'doctor').order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'patient__last_name', 'patient__first_name']
    ordering_fields = ['created_at', 'updated_at', 'title']
