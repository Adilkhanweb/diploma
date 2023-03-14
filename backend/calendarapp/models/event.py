from datetime import datetime
from django.db import models
from django.urls import reverse

from calendarapp.models import EventAbstract
from account.models import User


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter(is_active=True, is_deleted=False)
        return events

    def get_running_events(self):
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

    def get_events(self):
        events = Event.objects.filter(is_active=True, is_deleted=False, start_time__gte=datetime.now())


class Event(EventAbstract):
    """ Event model """

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=256, blank=True, null=True)

    objects = EventManager()

    def __str__(self):
        return self.title


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
