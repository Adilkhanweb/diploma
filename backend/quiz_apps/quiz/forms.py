from django import forms


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
