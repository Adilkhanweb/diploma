from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from account.models import Teacher


class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


