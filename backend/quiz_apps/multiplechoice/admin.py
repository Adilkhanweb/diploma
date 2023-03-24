from django import forms
from django.contrib import admin

from quiz_apps.multiplechoice.models import Answer, MultipleChoice


class AnswerInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        correct_answers = 0
        answers = 0
        for form in self.forms:
            try:
                if form.cleaned_data['correct']:
                    correct_answers += 1
                if form.cleaned_data:
                    answers += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if correct_answers < 1:
            raise forms.ValidationError('You must select at least one answers as correct')
        if correct_answers > 3:
            raise forms.ValidationError('You should select no more than 3 answers as correct')
        if answers != 6:
            raise forms.ValidationError('You must have 6 answer options')


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    max_num = 6
    min_num = 6
    formset = AnswerInlineFormset
    can_delete = False


class MultipleChoiceAdmin(admin.ModelAdmin):
    list_display = ('content', 'score')
    fields = ('content',
              'figure', 'quiz', 'explanation', 'answer_order', 'score', 'correct_answers_count')

    search_fields = ('content', 'explanation')
    readonly_fields = ('score', 'correct_answers_count')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]


admin.site.register(MultipleChoice, MultipleChoiceAdmin)
