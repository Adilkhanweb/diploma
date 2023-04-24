from django import forms

from problems.models import Problem, TestCase
from djangoformsetjs.utils import formset_media_js


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'slug', 'description', 'ex_input', 'ex_output', 'ex_description', 'difficulty', 'base_code',
                  'points', 'time_limit']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class TestCaseForm(forms.ModelForm):
    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )

    class Meta:
        model = TestCase
        fields = ['input', 'expected_output', 'is_hidden']
        widgets = {
            'input': forms.Textarea(attrs={'rows': '3', 'class': 'form-control'}),
            'expected_output': forms.Textarea(attrs={'rows': '3', 'class': 'form-control'})
        }
