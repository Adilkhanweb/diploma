# cal/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from calendarapp.models import EventMember, Event, RecurringEvent
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "users:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events()
        recurring_events = RecurringEvent.objects.all()
        events_month = Event.objects.get_running_events()
        event_list = []
        # start: '2020-09-16T16:00:00'
        """
        For recurrent events
        "title": event.title,
        "daysOfWeek": ['4'],
        "startTime": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "endTime": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "url": "/events/"
        """
        for event in events:
            if not event.start_time:
                event_list.append({
                    "title": event.title,
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "url": event.url,
                })
            elif event.url:
                event_list.append({
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "url": event.url,
                })
            else:
                event_list.append(
                    {
                        "title": event.title,
                        "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                )
        for event in recurring_events:
            event_list.append({
                "title": event.title,
                "startTime": event.time_start.strftime("%H:%M"),
                "endTime": event.time_end.strftime("%H:%M"),
                "startRecur": event.start_date.strftime("%Y-%m-%d"),
                "endRecur": event.end_date.strftime("%Y-%m-%d"),
                "daysOfWeek": f"[{event.days_of_week}]",
            })
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
