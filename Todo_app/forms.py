from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task
from django.core.exceptions import ValidationError
from datetime import date


# User Registration Form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Task Form
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'status', 'category', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter task title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter task details'}),
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',                  # browser date picker
                    'placeholder': 'Select due date',
                    'min': date.today().isoformat()  # prevent past dates
                }
            ),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < date.today():
            raise ValidationError("Due date cannot be in the past.")
        return due_date
