from django import forms

from assignment.models import AssignmentSubmission, Assignment, AssignmentSubmissionFiles
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['comment', ]
        # widgets = {
        #     'files': forms.ClearableFileInput(attrs={'multiple': True}),
        # }


class FileSubmissionForm(forms.Form):
    files = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 10)


class AssignmentForm(forms.ModelForm):
    """
    title
description
deadline
created_at
updated_at
    """

    class Meta:
        deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'auto_now_add': True}))
        model = Assignment
        fields = ['title', 'description', 'deadline']


class AssigmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['grade', ]
        widgets = {
            'grade': forms.NumberInput(attrs={'max': 100, 'min': 0, 'required': True, 'step': 10})
        }
