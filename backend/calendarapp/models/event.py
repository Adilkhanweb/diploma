from datetime import datetime
from django.db import models
from django.urls import reverse
from django.db.models import DateTimeField, ExpressionWrapper, F, Q
from django.db.models.functions import Coalesce
from assignment.models import Assignment
from calendarapp.models import EventAbstract
from quiz_apps.quiz.models import Quiz
from users.models import User
from django.utils import timezone


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter(is_active=True, is_deleted=False).annotate(
            latest_end_time=Coalesce(
                F('quiz__end_time'),
                F('assignment__deadline'),
                output_field=DateTimeField()
            )
        ).order_by('latest_end_time')
        return events

    def get_running_events(self):
        now = timezone.now()
        running_events = Event.objects.filter(is_active=True, is_deleted=False).filter(
            Q(quiz__end_time__gte=now) | Q(assignment__deadline__gte=now)).annotate(
            latest_end_time=Coalesce(
                F('quiz__end_time'),
                F('assignment__deadline'),
                output_field=DateTimeField()
            )
        ).order_by('latest_end_time')
        return running_events


def get_events(self):
    events = Event.objects.filter(is_active=True, is_deleted=False)
    return events


class Event(EventAbstract):
    """ Event model """

    quiz = models.ForeignKey(Quiz, related_name="quiz_events", null=True, on_delete=models.CASCADE, blank=True)
    assignment = models.ForeignKey(Assignment, related_name="assignment_events", null=True, on_delete=models.CASCADE,
                                   blank=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=256, blank=True, null=True)

    objects = EventManager()

    def __str__(self):
        if self.assignment:
            return f"Assignment Event: {self.assignment.title}"
        if self.quiz:
            return f"Quiz Event: {self.quiz.title}"
        else:
            return f"Event"


class RecurringEvent(EventAbstract):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    time_start = models.TimeField()
    time_end = models.TimeField()
    start_date = models.DateField(help_text="Recurring event start date")
    end_date = models.DateField(help_text="Recurring event end date")
    days_of_week = models.CharField(max_length=13,
                                    help_text="Days of week in which event will be recurring. Write comma separated "
                                              "list of weeks.Ex: 1,2. Here 1 is Monday")
    url = models.CharField(max_length=256, blank=True, null=True)
