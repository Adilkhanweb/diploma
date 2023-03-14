from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from quiz_apps.multiplechoice.models import Attempt, AttemptQuestion
from quiz_apps.quiz.forms import QuestionForm
from quiz_apps.quiz.models import Quiz, BaseQuestion


def check_attempts(quiz, user):
    return (quiz.start_time <= timezone.now() <= quiz.end_time) and \
        Attempt.objects.filter(quiz=quiz, user=user).count() < quiz.max_attempts


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(draft=False)
    return render(request, "quiz/quiz_list.html", {
        "quizzes": quizzes,
    })


@login_required
def quiz_detail(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    attempts = Attempt.objects.filter(quiz=quiz, user=request.user)
    can_attempt = check_attempts(quiz, request.user)
    return render(request, "quiz/quiz_detail.html", {
        "quiz": quiz,
        "available_attempts": quiz.max_attempts - attempts.count(),
        "can_attempt": can_attempt,
        "attempts": attempts
    })


@login_required
def attempt(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    forms = []
    if check_attempts(quiz, request.user):
        for question in quiz.get_questions():
            if question.figure:
                forms.append({"figure": question.figure.url,
                              "form": QuestionForm(question=question, auto_id=False, prefix=f"{question.id}")})
            else:
                forms.append(
                    {"figure": None, "form": QuestionForm(question=question, auto_id=False, prefix=f"{question.id}")})
        return render(request, "quiz/attempt.html", {
            "quiz": quiz,
            "forms": forms
        })
    else:
        return redirect('quiz:quiz_detail', quiz.url)


@login_required
def submit(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    questions = quiz.get_questions()
    answers = dict()
    if request.method == 'POST' and check_attempts(quiz, request.user):
        attempt = Attempt.objects.create(user=request.user, quiz=quiz)
        for question in questions.all():
            answers[question.id] = list(map(int, request.POST.getlist(f'{question.id}-answers')))
            correct_answers = list(question.answers.filter(correct=True).values_list('id', flat=True))
            # if we have all correct answers and no one incorrect
            if set(correct_answers).intersection(set(answers[question.id])) == set(correct_answers) and set(
                    answers[question.id]).difference(set(correct_answers)) == set():
                aq = AttemptQuestion.objects.create(attempt=attempt, question=question, is_correct=True)
            else:
                aq = AttemptQuestion.objects.create(attempt=attempt, question=question, is_correct=False)
            aq.given_answers.set(answers[question.id])
            aq.correct_answers.set(correct_answers)
            attempt.save()
        return HttpResponseRedirect(reverse('quiz:results', args=(quiz.url, attempt.id)))
    return redirect('quiz:quiz_detail', quiz.url)


def results(request, url, attempt_id, **kwargs):
    quiz = get_object_or_404(Quiz, url=url)
    attempt = get_object_or_404(Attempt, id=attempt_id)
    return render(request, "quiz/quiz_results.html", {"quiz": quiz, "attempt": attempt})
