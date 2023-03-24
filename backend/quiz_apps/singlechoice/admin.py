from django.contrib import admin
from django import forms

from quiz_apps.multiplechoice.models import Answer
from quiz_apps.quiz.models import BaseQuestion
from quiz_apps.singlechoice.models import Choice


# Register your models here.
class SingleCorrectAnswerInlineFormset(forms.models.BaseInlineFormSet):

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
        if correct_answers > 1:
            raise forms.ValidationError('You must have one correct answer')
        elif correct_answers == 0:
            raise forms.ValidationError('You must select one answer as correct')
        if answers != 4:
            raise forms.ValidationError('You must have 4 answer options')


class SingleCorrectAnswerInline(admin.TabularInline):
    model = Answer
    max_num = 4
    min_num = 4
    formset = SingleCorrectAnswerInlineFormset
    can_delete = False


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('content', 'score')
    fields = ('content',
              'figure', 'quiz', 'explanation', 'answer_order', 'score', 'correct_answers_count')

    search_fields = ('content', 'explanation')
    readonly_fields = ('score', 'correct_answers_count')
    filter_horizontal = ('quiz',)

    inlines = [SingleCorrectAnswerInline]


admin.site.register(Choice, ChoiceAdmin)
