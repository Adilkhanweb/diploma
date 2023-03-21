from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from calendarapp.models import Event
from course.models import Lesson
from diploma_backend.forms import LessonForm


class DashboardView(LoginRequiredMixin, View):
    login_url = "account:signin"
    template_name = "diploma_backend/dashboard.html"

    def get(self, request, *args, **kwargs):
        book_form = LessonForm(initial={"type": "book"})
        lesson_form = LessonForm(initial={"type": "lesson"})
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
            "book_form": book_form,
            "lesson_form": lesson_form,
        }

        return render(request, self.template_name, context)


def addBook(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.type = "book"
            lesson.save()
            return HttpResponseRedirect(request.path_info)
        else:
            print(form.errors)
            return redirect("dashboard")
    else:
        form = LessonForm()
    return redirect("dashboard")


def addLesson(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.type = "lesson"
            lesson.save()
            return redirect("dashboard")
        else:
            print(form.errors)
            return redirect("dashboard")
    else:
        form = LessonForm()
    return redirect("dashboard")
