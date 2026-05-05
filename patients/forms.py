from django import forms
from .models import Patient, Doctor


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'date_of_birth', 'phone', 'email', 'address']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'date_of_birth': 'Дата рождения',
            'phone': 'Телефон',
            'email': 'Email',
            'address': 'Адрес',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 900 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['last_name', 'first_name', 'specialization', 'phone', 'email']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'specialization': 'Специализация',
            'phone': 'Телефон',
            'email': 'Email',
        }
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 900 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
