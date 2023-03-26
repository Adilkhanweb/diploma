from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from users.models import Student


class StudentCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Құпия сөз",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Құпия сөзді растаңыз",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password],
    )

    class Meta:
        model = Student
        fields = ["email", "first_name", "last_name", "password1", "password2"]
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control"}),
                   "first_name": forms.TextInput(attrs={"class": "form-control"}),
                   "last_name": forms.TextInput(attrs={"class": "form-control"})}


# class StudentSignUpForm(forms.ModelForm):
#     password1 = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#         validators=[validate_password],
#     )
#     password2 = forms.CharField(
#         label="Confirm Password",
#         widget=forms.PasswordInput(attrs={"class": "form-control"}),
#         validators=[validate_password],
#     )
#
#     class Meta:
#         model = Student
#         fields = ["email", "first_name", "last_name"]
#         widgets = {"email": forms.EmailInput(attrs={"class": "form-control"}),
#                    "first_name": forms.TextInput(attrs={"class": "form-control"}),
#                    "last_name": forms.TextInput(attrs={"class": "form-control"})}

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Password didn't match!")
    #     return password2

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
