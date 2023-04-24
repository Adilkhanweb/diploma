import json
import re

from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import MaxValueValidator, validate_comma_separated_integer_list
from django.db.models import Sum, Max
from django.urls import reverse
from django.utils import timezone
from model_utils.managers import InheritanceManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class Quiz(models.Model):
    title = models.CharField(
        verbose_name="Атауы",
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name="Сипаттама",
        blank=True, help_text="Бақылаудың қысқаша сипаттамасы")

    url = models.SlugField(
        max_length=60, blank=False,
        help_text="бақылауға сілтеме",
        verbose_name="Сілтеме")

    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name="Рандомды тәртіппен",
        help_text="Сұрақтарды кездейсоқ ретпен немесе олар орнатылған ретпен көрсету керек пе?")
    max_attempts = models.PositiveIntegerField(null=True, verbose_name="Әрекеттердің рұқсат етілген саны",
                                               default=1)

    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name="Өту балы",
        help_text="Сәтті тапсыру үшін қажетті пайыз",
        validators=[MaxValueValidator(100)])

    success_text = models.TextField(
        blank=True, help_text=_("Егер пайдаланушы сәтті тапсырса, көрсетілетін мәтін."),
        verbose_name="Сәтті мәтіні")

    fail_text = models.TextField(
        verbose_name="Сәтсіз мәтіні",
        blank=True, help_text="Егер пайдаланушы сәтсіз тапсырса, көрсетілетін мәтін.")
    draft = models.BooleanField(
        blank=True, default=False,
        verbose_name="Уақытша",
        help_text='Олай болса, тест тесттер тізімінде көрсетілмейді және оны тек тестілерді өңдей алатын пайдаланушылар ғана тапсыра алады.')
    start_time = models.DateTimeField(verbose_name="Басталу уақыты")
    end_time = models.DateTimeField(verbose_name="Аяқталу уақыты")
    duration = models.DurationField(default=timezone.timedelta(hours=2), verbose_name="Уақыт",
                                    help_text="Тапсыруға берілетін уақыт")

    @property
    def is_passed(self):
        return timezone.now() > self.end_time

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.pass_mark > 100:
            raise ValidationError('%s is above 100' % self.pass_mark)
        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quiz:quiz_detail', args=[str(self.url)])

    def get_questions(self):
        questions = self.questions.all().select_subclasses()
        if self.random_order:
            return questions.order_by('?')
        return questions

    def get_max_scores(self):
        scores = self.questions.aggregate(Sum('score'))['score__sum']
        return scores


class BaseQuestion(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """
    quiz = models.ManyToManyField(Quiz,
                                  verbose_name="Бақылау",
                                  blank=True, related_name="questions")

    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               verbose_name="Фото")

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text="Көрсеткіңіз келетін сұрақтың мәтінін енгізіңіз",
                               verbose_name="Сұрақ")

    explanation = CKEditor5Field("Түсіндірме", blank=True,
                                 config_name='student')

    score = models.PositiveIntegerField(default=1)
    correct_answers_count = models.PositiveIntegerField(default=1)
    objects = InheritanceManager()

    class Meta:
        verbose_name = "Сұрақ"
        verbose_name_plural = "Сұрақтар"

    def __str__(self):
        return self.content
