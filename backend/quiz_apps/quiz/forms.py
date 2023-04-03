from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from quiz_apps.multiplechoice.models import AttemptQuestion
from quiz_apps.quiz.models import Quiz, BaseQuestion
from quiz_apps.quiz.widgets import CustomRadioSelect, CustomCheckboxSelectMultiple
from durationwidget.widgets import TimeDurationWidget


# class ChoiceForm(forms.ModelForm):
#     def __init__(self, question, *args, **kwargs):
#         super(ChoiceForm, self).__init__(*args, **kwargs)
#         self.fields['answers'] = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=question.answers)
#
#     class Meta:
#         model = Choice
#         fields = "__all__"
#
#
# class MultipleChoiceForm(forms.ModelForm):
#     def __init__(self, question, *args, **kwargs):
#         super(MultipleChoiceForm, self).__init__(*args, **kwargs)
#         self.fields['answers'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
#                                                                 queryset=question.answers)
#
#     class Meta:
#         model = MultipleChoice
#         fields = "__all__"


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if question.answers.count() > 4:
            self.fields['answers'] = forms.ModelMultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(
                    attrs={"id": "id-checkbox"}),
                queryset=question.answers)
            self.fields["answers"].label = question.content
        else:
            self.fields['answers'] = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=question.answers,
                                                            required=False)
            self.fields["answers"].label = question.content


class AttemptQuestionForm(forms.ModelForm):

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance.question.answers.count() > 4:
            self.fields['given_answers'] = forms.ModelMultipleChoiceField(
                widget=CustomCheckboxSelectMultiple(
                    attrs={}),
                queryset=instance.question.answers, initial=list(map(lambda x: x.id, instance.given_answers.all())),
                label='', )

        else:
            self.fields['given_answers'] = forms.ModelChoiceField(widget=CustomRadioSelect,
                                                                  queryset=instance.question.answers,
                                                                  initial=list(map(lambda x: x.id,
                                                                                   instance.given_answers.all())),
                                                                  required=False, label='')

    class Meta:
        model = AttemptQuestion
        fields = ('given_answers',)


class QuizForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    draft = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    random_order = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    pass_mark = forms.IntegerField(widget=forms.NumberInput(attrs={'step': 10, 'min': 0, 'max': 100, 'value': 0,
                                                                   'class': 'form-control'}))
    max_attempts = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10, 'value': 1, 'class': 'form-control'}))
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    duration = forms.DurationField(widget=TimeDurationWidget(attrs={'class': 'form-control'}))

    questions = forms.ModelMultipleChoiceField(
        queryset=BaseQuestion.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}))

    class Meta:
        model = Quiz
        fields = (
            'title', 'description', 'url', 'random_order', 'max_attempts', 'success_text', 'fail_text', 'draft',
            'pass_mark',
            'start_time', 'end_time',
            'duration', 'questions')

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.questions.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizForm, self).save(commit=False)
        quiz.save()
        quiz.questions.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz
