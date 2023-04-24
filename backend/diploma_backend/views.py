from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, PermissionsMixin

from calendarapp.models import Event
from course.models import Lesson
from diploma_backend.forms import LessonForm
from django.contrib.auth.decorators import login_required, user_passes_test

from users.forms import UserCreationFormForAdmin
from users.models import User


class MainPageView(TemplateView):
    template_name = "diploma_backend/home_page.html"


class DashboardView(LoginRequiredMixin, View):
    login_url = "users:signin"
    template_name = "diploma_backend/dashboard.html"

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.first()
        book_form = LessonForm(initial={"type": "book"})
        lesson_form = LessonForm(initial={"type": "lesson"})
        lessons = Lesson.objects.filter(type="lesson").order_by('-created_at')
        books = Lesson.objects.filter(type="book").order_by('-created_at')
        events = Event.objects.get_all_events()
        running_events = Event.objects.get_running_events()
        latest_events = Event.objects.filter().order_by("-id")[:10]
        context = {
            "lesson": lesson,
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
                          {"books": Lesson.objects.filter(type='book').order_by('-created_at')})
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
                          {'lessons': Lesson.objects.filter(type="lesson").order_by('-created_at'),
                           'lesson_form': LessonForm()})
    else:
        return HttpResponse(status=400)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Teacher').count() == 0, login_url='users:signin')
def update_lesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = LessonForm(instance=lesson)
        if lesson.type == 'lesson':
            return render(request, 'diploma_backend/partials/lesson-change-form.html',
                          {'lesson_form': form, 'lesson': lesson})
        else:
            return render(request, 'diploma_backend/partials/book-change-form.html',
                          {'book_form': form, 'book': lesson})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Teacher').count() == 0, login_url='users:signin')
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    books = Lesson.objects.filter(type="book")
    lessons = Lesson.objects.filter(type="lesson").order_by('-created_at')
    if lesson.type == 'book':
        lesson.delete()
        return render(request, "diploma_backend/partials/books-list.html", {'books': books})
    else:
        lesson.delete()
        return render(request, "diploma_backend/partials/lessons-list.html", {'lessons': lessons})


def handler404(request, exception):
    return render(request, 'base/404.html', status=404)


def handler500(request):
    return render(request, 'base/500.html', status=500)


def lessons_list(request):
    lessons = Lesson.objects.filter(type="lesson").order_by('-created_at')
    return render(request, "diploma_backend/partials/lessons-list.html", {'lessons': lessons})


def books_list(request):
    books = Lesson.objects.filter(type="book").order_by('-created_at')
    return render(request, "diploma_backend/partials/books-list.html", {'books': books})


def create_user(request):
    form = UserCreationFormForAdmin()
    if request.method == 'POST':
        form = UserCreationFormForAdmin(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            group = form.cleaned_data['group']
            user.save()
            user.groups.set([group.id])
            return redirect('users')
        else:
            return render(request, "diploma_backend/create-user.html", {'form': form})
    return render(request, "diploma_backend/create-user.html", {'form': form})


def user_list(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, "diploma_backend/users.html", {'users': users})
