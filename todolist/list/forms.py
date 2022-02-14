from django.forms import ModelForm
from .models import Task
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=64, help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
