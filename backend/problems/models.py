from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from datetime import datetime
import operator


class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Problem(Time):
    class Difficulty(models.IntegerChoices):
        EASY = 1, _("Оңай")
        MEDIUM = 2, _("Орташа")
        HARD = 3, _("Қиын")

    title = models.CharField(max_length=128, verbose_name="Атауы")
    slug = models.SlugField(unique=True, verbose_name="Сілтемесі")
    description = models.TextField(max_length=1000, null=True, verbose_name="Сипаттама")
    ex_input = models.TextField(max_length=1000, null=True, verbose_name="Кіріс дерегі мысалы")
    ex_output = models.TextField(max_length=1000, null=True, verbose_name="Шығу мысалы")
    ex_description = models.TextField(max_length=1000, null=True, verbose_name="Мысал түсіндірмесі")
    difficulty = models.IntegerField(max_length=128, choices=Difficulty.choices, default=Difficulty.EASY,
                                     verbose_name="Қиындығы")
    base_code = models.TextField(null=True, blank=True, verbose_name="Бастапқы берілген код")
    points = models.PositiveSmallIntegerField(default=1, verbose_name="Балл")
    testcases_count = models.PositiveSmallIntegerField(default=0)
    time_limit = models.FloatField(default=3, help_text="Кодты орындауға кететін уақыт (секундпен)",
                                   verbose_name="Уақыт шегі")

    class Meta:
        verbose_name = _("Бағдаламалау Мәселесі")
        verbose_name_plural = _("Бағдарламалау Мәселелері")

    def __str__(self):
        return self.title


class TestCase(Time):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="testcases")
    input = models.TextField(verbose_name="Кіріс дерегі")
    expected_output = models.TextField(verbose_name="Күтілген нәтиже")
    is_hidden = models.BooleanField(default=True, verbose_name="Жабық сынақ?",
                                    help_text="Кіріс ж-е шығыс деректері қолданушыға көрінбейді")

    class Meta:
        verbose_name = "Бағдарламалау Сынағы"
        verbose_name_plural = "Бағдарламалау Сынақтары"

    def __str__(self):
        return f'{self.input}: {self.expected_output}'


class Submission(Time):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_code = models.TextField()
    avg_time = models.CharField(max_length=20, blank=True, null=True)
    avg_memory = models.IntegerField(blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    success_testcases = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.problem.title
