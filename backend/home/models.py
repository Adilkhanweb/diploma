import datetime

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import InlinePanel, FieldPanel
from wagtail.documents.models import Document
from wagtail.fields import RichTextField

from wagtail.models import Page, Orderable
#
# from course.forms import AssignmentSubmissionForm
from course.models import Lesson


# from home.forms import AssignmentForm


class HomePage(Page):
    pass


class Dashboard(Page):
    pass

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['lessons'] = Lesson.objects.filter(type='lesson')
        context['books'] = Lesson.objects.filter(type='book')
        return context

    def serve(self, request, *args, **kwargs):
        return super(Dashboard, self).serve(request, *args, **kwargs)

#
# class Homework(Page):
#     template = "course/templates/homework.html"
#     pass
