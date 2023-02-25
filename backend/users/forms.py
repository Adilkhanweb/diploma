from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm
from allauth.account.forms import SignupForm


class CustomUserEditForm(UserEditForm):
    is_teacher = forms.BooleanField(required=True, label=_("is Teacher"))


class CustomUserCreationForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=True, label=_("is Teacher"))


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
