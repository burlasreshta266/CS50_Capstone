from django import forms
from django.contrib.auth.models import User
from .models import Project, Technology


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'short_description', 'long_description', 'status', 'technologies']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'placeholder': 'Enter project title'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'placeholder': 'Enter short description'
            }),
            'long_description': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'placeholder': 'Enter detailed description',
                'rows': 4
            }),
            'status': forms.Select(attrs={
                'class': 'form-control w-100',
            }),
            'technologies': forms.SelectMultiple(attrs={
                'class': 'form-control w-100',
            })
        }


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter new technology name',
                'id': 'new-tech-name'  # ID for easy JS access
            })
        }


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'placeholder': 'Enter username'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])   # hash password
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Enter password'
    }))
