from django import forms
from django.forms import BaseFormSet

from quiz_apps.multiplechoice.models import AttemptQuestion, Answer
from quiz_apps.quiz.models import BaseQuestion


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
                widget=forms.CheckboxSelectMultiple(
                    attrs={}),
                queryset=instance.question.answers, initial=list(map(lambda x: x.id, instance.given_answers.all())))
            self.fields["given_answers"].label = instance.question.content

        else:
            self.fields['given_answers'] = forms.ModelChoiceField(widget=forms.RadioSelect,
                                                                  queryset=instance.question.answers,
                                                                  initial=list(map(lambda x: x.id,
                                                                                   instance.given_answers.all())),
                                                                  required=False)
            self.fields["given_answers"].label = instance.question.content

    # given_answers = forms.ModelMultipleChoiceField(queryset=Answer.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = AttemptQuestion
        fields = ('given_answers',)
