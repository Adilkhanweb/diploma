from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
# Create your models here.
from wagtail.admin.panels import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField, RichTextField
from users.models import Teacher, Student
from streams import blocks


class Lesson(models.Model):
    class Types(models.TextChoices):
        LESSON = 'lesson', 'Lesson'
        BOOK = 'book', 'Book'

    title = models.CharField(max_length=128)
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.LESSON, null=True)
    banner = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.CASCADE, related_name='+')
    description = RichTextField()
    document = models.ForeignKey(
        'wagtaildocs.Document', on_delete=models.CASCADE, related_name='+'
    )

    def __str__(self):
        return f"{self.title}"

    panels = [
        FieldPanel("title"),
        FieldPanel("banner"),
        FieldPanel("type"),
        FieldPanel("description"),
        FieldPanel("document"),
    ]


class Assignment(models.Model):
    title = models.CharField(max_length=128)
    description = RichTextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("deadline"),
    ]

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=False, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, verbose_name=_("Тапсырма атауы"))
    files = models.FileField(upload_to="assignment/", verbose_name=_("Файлдар"))
    created_at = models.DateTimeField(auto_now_add=True)
