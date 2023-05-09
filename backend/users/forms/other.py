from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from users.models import Profile, User, Consultation
from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm


class UserCreationFormForAdmin(UserCreationForm):
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

    last_name = forms.CharField(label="Тегі")
    email = forms.EmailField(label="Электрондық пошта")

    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Топ",
                                   required=True, widget=forms.RadioSelect)

    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "password1", "password2", "group"]
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control"}),
                   "first_name": forms.TextInput(attrs={"class": "form-control"}),
                   "last_name": forms.TextInput(attrs={"class": "form-control"})}


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class MyCustomSocialSignupForm(SignupForm):

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save(request)
        if not user.is_superuser:
            students_group, created = Group.objects.get_or_create(name="Students")
            user.groups.set([students_group])
            profile, created = Profile.objects.get_or_create(user=user)
        # Add your own processing here.

        # You must return the original result.
        return user


class ProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={"id": "profile-picture-box"}))

    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'email')
        fields = ('first_name', 'last_name')


class PasswordUpdateForm(PasswordChangeForm):
    pass


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = '__all__'
