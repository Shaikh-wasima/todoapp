from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Task

class CustomUserCreationForm(UserCreationForm):
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'is_admin']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'assigned_to']
