from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models import Event
from course.models import Lesson


class DashboardView(LoginRequiredMixin, View):
    login_url = "account:signin"
    template_name = "diploma_backend/dashboard.html"

    def get(self, request, *args, **kwargs):
        lessons = Lesson.objects.filter(type="lesson")
        books = Lesson.objects.filter(type="book")
        events = Event.objects.get_all_events()
        running_events = Event.objects.get_running_events()
        latest_events = Event.objects.filter().order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "lessons": lessons,
            "books": books,
        }
        return render(request, self.template_name, context)
