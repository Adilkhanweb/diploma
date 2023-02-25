from django import forms
from django.forms import ClearableFileInput
from .models import Assignment, AssignmentSubmission


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'files', 'user']
        widgets = {
            'files': ClearableFileInput(attrs={'multiple': True}),
            'assignment': forms.RadioSelect(attrs={'hidden': True}),
            'user': forms.RadioSelect(attrs={'hidden': True}),
        }
