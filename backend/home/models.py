import itertools

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


class HomePage(Page):
    body = RichTextField(null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('testimonials', label="Testimonials"),
    ]

    api_fields = [
        APIField("body"),
        APIField("testimonials"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        test = grouper(3, self.testimonials.all())
        context['testims'] = test
        return context


class Testimonial(Orderable):
    page = ParentalKey(HomePage, on_delete=models.SET_NULL, null=True, related_name="testimonials")
    student_name = models.CharField(max_length=128)
    student_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    university = models.CharField(max_length=128, help_text="Place of study of the graduating student")
    body = RichTextField(features=["bold", "italic"])

    panels = [
        FieldPanel('student_name'),
        FieldPanel('student_photo'),
        FieldPanel('university'),
        FieldPanel('body'),
    ]

    api_fields = [
        APIField("student_name"),
        APIField("student_photo"),
        APIField("university"),
        APIField("body"),
    ]
