from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Patient, Doctor


class PatientSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False, allow_blank=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'date_of_birth',
                  'phone', 'email', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']


class DoctorSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False, allow_blank=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialization', 'phone', 'email']
        read_only_fields = ['id']
