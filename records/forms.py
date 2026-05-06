from django import forms
from .models import MedicalRecord


class MedicalRecordForm(forms.ModelForm):
    # Явно объявляем поле, чтобы Django принимал формат datetime-local (YYYY-MM-DDTHH:MM)
    appointment_time = forms.DateTimeField(
        required=False,
        label='Время записи',
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'appointment_time', 'title', 'description', 'diagnosis']
        labels = {
            'patient': 'Пациент',
            'doctor': 'Врач',
            'appointment_time': 'Время записи',
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
