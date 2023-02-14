from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable


class CoursesIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['courses'] = Course.objects.filter(owner__exact=request.user)
        return context


class Course(Page):
    template = "courses/course.html"
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        InlinePanel('lessons', label="Lessons"),
    ]


class Lesson(Orderable):
    page = ParentalKey(Course, on_delete=models.SET_NULL, null=True, related_name="lessons")
    title = models.CharField(max_length=128)
    content = RichTextField()
