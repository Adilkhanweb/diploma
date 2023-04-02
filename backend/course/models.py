import os

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Lesson(models.Model):
    class Types(models.TextChoices):
        LESSON = 'lesson', _('Lesson')
        BOOK = 'book', _('Book')

    title = models.CharField(max_length=128)
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.LESSON, null=True)
    banner = models.ImageField(upload_to="images/")
    description = models.TextField()
    document = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    @property
    def document_name(self):
        return os.path.basename(self.document.name)
