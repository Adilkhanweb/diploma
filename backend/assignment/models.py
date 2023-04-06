import os

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from users.models import Student, User
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
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    assignment = models.OneToOneField(Assignment, on_delete=models.SET_NULL, null=True,
                                      verbose_name=_("Тапсырма атауы"), related_name="submissions")
    comment = models.TextField(_("Сипаттама"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    graded = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return self.assignment.title


class AssignmentSubmissionFiles(models.Model):
    assignment_submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="assignment/", verbose_name=_("Файлдар"), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
