from rest_framework import serializers
from .models import MedicalRecord, Report


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
                  'title', 'description', 'diagnosis', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
                  'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
