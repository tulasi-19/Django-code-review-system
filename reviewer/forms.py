from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CodeSubmission


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = CodeSubmission
        fields = ["title", "language", "code"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Assignment 3 - Binary Search"}),
            "language": forms.Select(attrs={"class": "form-select"}),
            "code": forms.Textarea(attrs={"class": "form-control code-textarea", "rows": 16, "spellcheck": "false"}),
        }
