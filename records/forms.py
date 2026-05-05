from django import forms
from .models import MedicalRecord


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'title', 'description', 'diagnosis']
        labels = {
            'patient': 'Пациент',
            'doctor': 'Врач',
            'title': 'Заголовок',
            'description': 'Описание',
            'diagnosis': 'Диагноз',
        }
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'diagnosis': forms.TextInput(attrs={'class': 'form-control'}),
        }
