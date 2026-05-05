from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['institution', 'position']
        labels = {
            'institution': 'Медучреждение',
            'position': 'Должность',
        }
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ГБУЗ «Городская поликлиника №1»'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Главный врач'}),
        }
