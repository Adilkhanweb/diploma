from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from calendarapp.models import Event
from course.models import Lesson
from diploma_backend.forms import LessonForm
from django.contrib.auth.decorators import login_required, user_passes_test


class DashboardView(LoginRequiredMixin, View):
    login_url = "users:signin"
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


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Teacher').count() == 0, login_url='users:signin')
def addBook(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.type = "book"
            lesson.save()
            return render(request, "diploma_backend/partials/books-list.html",
                          {"books": Lesson.objects.filter(type='book')})
    else:
        return HttpResponse(status=400)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Teacher').count() == 0, login_url='users:signin')
def addLesson(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.type = "lesson"
            lesson.save()
            return render(request, 'diploma_backend/partials/lessons-list.html',
                          {'lessons': Lesson.objects.filter(type="lesson"), 'lesson_form': LessonForm()})
    else:
        return HttpResponse(status=400)


def handler404(request, *args, **argv):
    response = render("base/404.html", request, {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render("base/500.html", request, {})
    response.status_code = 500
    return response
