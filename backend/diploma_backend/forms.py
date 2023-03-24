from django import forms

from course.models import Lesson


class LessonForm(forms.ModelForm):
    type = forms.CharField(widget=forms.TextInput(attrs={'hidden': 'true'}))
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Атауы'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'id': 'add-lesson-textarea', 'rows': 2,
               'placeholder': 'Қысқаша сипаттама'}), required=False)
    document = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Файл'}))

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'type', 'document', 'banner']
