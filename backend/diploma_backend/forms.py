from django import forms

from course.models import Lesson
from django.db import models


class ConsultationForm(forms.Form):
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    grade = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 9, 'max': 11}))
    phone_number = forms.CharField(max_length=25)
    email = forms.EmailField()


class LessonForm(forms.ModelForm):
    type = forms.CharField(widget=forms.TextInput(attrs={'hidden': 'true'}))
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Атауы'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control form-control-sm', 'rows': 2,
               'placeholder': 'Қысқаша сипаттама'}), required=False)
    document = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Файл'}))

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'type', 'document', 'banner']


class SearchForm(forms.Form):
    page_choices = (
        ('course-materials', 'Курс Материалдары'),
        ('quiz', 'Бақылау'),
        ('assignment', 'Үй жұмысы'),
        ('discussion', 'Талқылау'),
        ('programming', 'Бағдарламалау'),
    )
    page = forms.ChoiceField(choices=page_choices, widget=forms.Select(attrs={'class': 'form-select w-100 h-100',
                                                                              'style': 'border-top-right-radius: 0; border-bottom-right-radius: 0;'}))
    q = forms.CharField(max_length=120, widget=forms.TextInput(
        attrs={'type': 'search', 'placeholder': 'Іздеу...', 'class': 'form-control form-control-lg bg-muted-lt'}),
                        required=False)
