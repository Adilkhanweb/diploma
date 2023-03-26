from django import forms

from assignment.models import AssignmentSubmission, Assignment


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'files', 'user']
        widgets = {
            'files': forms.ClearableFileInput(attrs={'multiple': True}),
            'assignment': forms.RadioSelect(attrs={'hidden': True}),
            'user': forms.RadioSelect(attrs={'hidden': True}),
        }


class AssignmentForm(forms.ModelForm):
    """
    title
description
deadline
created_at
updated_at
    """

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'deadline']

