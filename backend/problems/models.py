from django.contrib.auth import get_user_model
from django.db import models

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
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=1000, null=True)
    explanation = models.TextField()
    base_code = models.TextField(null=True)

    def __str__(self):
        return self.title


class TestCase(Time):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="testcases")
    input = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.input}: {self.expected_output}'


class Submission(Time):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_code = models.TextField()
    avg_time = models.CharField(max_length=20, blank=True, null=True)
    avg_memory = models.IntegerField(blank=True, null=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.problem.title
