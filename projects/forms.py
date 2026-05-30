from django import forms
from .models import Project

INPUT_ATTRS = {'class': 'form-input'}


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'name': forms.TextInput(attrs=INPUT_ATTRS),
            'description': forms.Textarea(attrs={**INPUT_ATTRS, 'rows': 5}),
            'github_url': forms.URLInput(attrs=INPUT_ATTRS),
            'status': forms.Select(
                attrs={'class': 'form-input'},
                choices=[('open', 'Открыт'), ('closed', 'Закрыт')],
            ),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url', '')
        if url and 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url
