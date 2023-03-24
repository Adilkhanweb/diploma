import os

from django.db import models
from django.urls import reverse

from account.models import Student
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return reverse('assignments:assignment_detail', kwargs={'assignment_id': self.id})


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=False, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, verbose_name=_("Тапсырма атауы"))
    files = models.FileField(upload_to="assignment/", verbose_name=_("Файлдар"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.files.name)

    def __str__(self):
        return self.assignment.title
