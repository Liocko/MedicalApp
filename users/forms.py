from django import forms
from django.contrib.auth import authenticate, update_session_auth_hash

from .models import User


INPUT_ATTRS = {'class': 'form-input'}


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=124, widget=forms.TextInput(attrs=INPUT_ATTRS))
    surname = forms.CharField(max_length=124, widget=forms.TextInput(attrs=INPUT_ATTRS))
    email = forms.EmailField(widget=forms.EmailInput(attrs=INPUT_ATTRS))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = User(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
        )
        user.set_password(data['password1'])
        user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs=INPUT_ATTRS))
    password = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS))

    def authenticate_user(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        widgets = {
            'name': forms.TextInput(attrs=INPUT_ATTRS),
            'surname': forms.TextInput(attrs=INPUT_ATTRS),
            'about': forms.Textarea(attrs={**INPUT_ATTRS, 'rows': 4}),
            'phone': forms.TextInput(attrs=INPUT_ATTRS),
            'github_url': forms.URLInput(attrs=INPUT_ATTRS),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone

        if phone.startswith('8') and len(phone) == 11 and phone[1:].isdigit():
            phone = '+7' + phone[1:]
        elif phone.startswith('+7') and len(phone) == 12 and phone[2:].isdigit():
            pass
        else:
            raise forms.ValidationError(
                'Неверный формат номера телефона. Используйте 8XXXXXXXXXX или +7XXXXXXXXXX'
            )

        qs = User.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот номер телефона уже используется')

        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url', '')
        if not url:
            return url
        if 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs=INPUT_ATTRS))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError('Неверный текущий пароль')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
