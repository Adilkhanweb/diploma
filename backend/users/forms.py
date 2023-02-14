from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group


class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['role'] = forms.ModelChoiceField(required=True, queryset=Group.objects.all(),
                                                     widget=forms.RadioSelect())
        self.fields['first_name'] = forms.CharField(required=True)
        self.fields['last_name'] = forms.CharField(required=True)

    def save(self, request):
        # print(type(self.cleaned_data.pop('role')))
        user = super(MyCustomSignupForm, self).save(request)
        user.groups.add(self.cleaned_data.pop('role'))
        return user
