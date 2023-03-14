from django.contrib import admin

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from quiz_apps.multiplechoice.models import Attempt, AttemptQuestion, Answer
from quiz_apps.quiz.models import BaseQuestion, Quiz
from quiz_apps.singlechoice.models import Choice


class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=BaseQuestion.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.questions.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.questions.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title',)
    search_fields = ('description',)


class AttemptQuestionInline(admin.TabularInline):
    model = AttemptQuestion
    extra = 0


class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'is_passed', 'percentage',)
    inlines = [AttemptQuestionInline, ]


class AttemptQuestionAdmin(admin.ModelAdmin):
    # form = AttemptQuestionForm
    list_display = ('attempt', 'question', 'is_correct',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "given_answers":
            # Get the question id from the attempt question
            attempt_question_id = request.resolver_match.kwargs.get("object_id")
            attempt_question = AttemptQuestion.objects.get(id=attempt_question_id)
            question_id = attempt_question.question.id

            # Filter the answers queryset based on the question id
            kwargs["queryset"] = Answer.objects.filter(question_id=question_id)
        if db_field.name == "correct_answers":
            # Get the question id from the attempt question
            attempt_question_id = request.resolver_match.kwargs.get("object_id")
            attempt_question = AttemptQuestion.objects.get(id=attempt_question_id)
            question_id = attempt_question.question.id

            # Filter the answers queryset based on the question id
            kwargs["queryset"] = Answer.objects.filter(question_id=question_id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(AttemptQuestion, AttemptQuestionAdmin)
