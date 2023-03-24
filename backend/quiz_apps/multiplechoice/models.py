from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django.db import models
from quiz_apps.quiz.models import BaseQuestion, Quiz

ANSWER_ORDER_OPTIONS = (
    ('content', _('Content')),
    ('random', _('Random')),
    ('none', _('None'))
)


class MultipleChoice(BaseQuestion):
    answer_order = models.CharField(
        max_length=30, null=True, blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
        verbose_name=_("Answer Order"))

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_correct_answers(self):
        return self.answers.filter(question=self, correct=True)

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


class Answer(models.Model):
    question = models.ForeignKey(BaseQuestion, verbose_name=_("Question"), on_delete=models.CASCADE,
                                 related_name="answers")

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class Attempt(models.Model):
    class AttemptStatus(models.TextChoices):
        ATTEMPTED = "attempted", _("Attempted")
        ATTEMPTING = "attempting", _("Attempting")
        NOT_ATTEMPTED = "not", _("NotAttempted")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    found_questions = models.ManyToManyField(BaseQuestion, related_name="found_questions")
    is_passed = models.BooleanField(default=False)
    percentage = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=AttemptStatus.choices, default=AttemptStatus.NOT_ATTEMPTED)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.quiz.title} {self.user.first_name} {self.id}"

    def get_attempt_score(self):
        scores = self.attemptquestion_set.aggregate(Sum('score'))['score__sum']
        return scores


class AttemptQuestion(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    question = models.ForeignKey(BaseQuestion, on_delete=models.CASCADE, blank=True, null=True)
    given_answers = models.ManyToManyField(Answer, related_name="given_answers", blank=True, null=True)
    correct_answers = models.ManyToManyField(Answer, related_name="correct_answers", blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question.content}"
