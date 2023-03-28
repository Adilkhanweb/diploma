from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import JsonResponse, HttpResponse

from quiz_apps.multiplechoice.models import Attempt, AttemptQuestion
from quiz_apps.quiz.forms import AttemptQuestionForm
from quiz_apps.quiz.models import Quiz
from django.shortcuts import render

from quiz_apps.quiz.utils import check_attempts, get_score, is_correct


# from formtools.wizard.views import SessionWizardView


def save_question(request, url, id):
    attemptQuestion = AttemptQuestion.objects.get(id=id)
    if request.method == 'POST':
        given_answers = list(map(int, request.POST.getlist(f"{attemptQuestion.id}-given_answers")))
        attemptQuestion.given_answers.set(given_answers)
        correct_answers = list(attemptQuestion.question.answers.filter(correct=True).values_list('id', flat=True))
        # if we have all correct answers and no one incorrect
        if is_correct(given_answers, correct_answers):
            attemptQuestion.is_correct = True
            attemptQuestion.score = get_score(correct_answers, given_answers)
        else:
            attemptQuestion.is_correct = False
            attemptQuestion.score = get_score(correct_answers, given_answers)
        attemptQuestion.save()
        return HttpResponse(status=204)


def submit_attempt(request, url, attempt_id):
    attempt = Attempt.objects.get(id=attempt_id)
    attempt.status = Attempt.AttemptStatus.ATTEMPTED
    attempt.completed_at = timezone.now()
    attempt.save()
    return redirect('quiz:results', url=url, attempt_id=attempt_id)


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(draft=False, end_time__gt=timezone.now())
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
    quiz = Quiz.objects.get(url=url)
    if check_attempts(quiz, request.user):
        attempt, created = Attempt.objects.get_or_create(user=request.user, quiz=quiz,
                                                         status=Attempt.AttemptStatus.ATTEMPTING)
        quiz_end_time = attempt.created_at + quiz.duration
        attemptQuestions = attempt.attemptquestion_set.all()
        paginator = Paginator(attemptQuestions, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        forms = []
        for attemptQuestion in page_obj.object_list:
            forms.append(
                {"form": AttemptQuestionForm(instance=attemptQuestion, prefix=f"{attemptQuestion.id}"),
                 "attempt_question_id": attemptQuestion.id, "figure": (attemptQuestion.question.figure or None)})
        return render(request, 'quiz/attempt.html',
                      {'quiz': quiz, 'forms': forms, 'attempt': attempt, "page_obj": page_obj,
                       "quiz_end_time": quiz_end_time})
    else:
        return redirect('quiz:quiz_detail', quiz.url)


#
# @login_required
# def attempt(request, url):
#     quiz = get_object_or_404(Quiz, url=url)
#     forms = []
#     if check_attempts(quiz, request.user):
#         for question in quiz.get_questions():
#             if question.figure:
#                 forms.append({"figure": question.figure.url,
#                               "form": QuestionForm(question=question, auto_id=False, prefix=f"{question.id}")})
#             else:
#                 forms.append(
#                     {"figure": None, "form": QuestionForm(question=question, auto_id=False, prefix=f"{question.id}")})
#         return render(request, "quiz/attempt.html", {
#             "quiz": quiz,
#             "forms": forms
#         })
#     else:
#         return redirect('quiz:quiz_detail', quiz.url)

"""
@todo Куиз страницасында әр сұрақты бөлек сабмит жасай алатындай қылу керек.
Ол үшін әр сұраққа AttempQuestion создать етіп user-дің ответін әр өзгерісте given_answer-ге сақтау керек.
View параметріне quiz_url question_id, формадан answers алып AttemptQuestion get_or_create жасау керек.

"""


# def submit_question(request, url, question_id):
#     quiz = get_object_or_404(Quiz, url=url)
#     question = get_object_or_404(BaseQuestion, id=question_id)
#     if request.method == 'POST' and check_attempts(quiz, request.user):
#         attempt = Attempt.objects.get(quiz=quiz, user=request.user, status=Attempt.AttemptStatus.ATTEMPTING)
#         answers = list(map(int, request.POST.getlist(f'{question.id}-answers')))
#         attempt_question = AttemptQuestion.objects.get_or_create(attempt=attempt, question=question, answers=answers)


@login_required
def submit(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    questions = quiz.get_questions()
    answers = dict()
    if request.method == 'POST' and check_attempts(quiz, request.user):
        attempt = Attempt.objects.get(user=request.user, quiz=quiz, status=Attempt.AttemptStatus.ATTEMPTING)
        for question in questions.all():
            answers[question.id] = list(map(int, request.POST.getlist(f'{question.id}-answers')))
            correct_answers = list(question.answers.filter(correct=True).values_list('id', flat=True))
            # if we have all correct answers and no one incorrect
            if set(correct_answers).intersection(set(answers[question.id])) == set(correct_answers) and set(
                    answers[question.id]).difference(set(correct_answers)) == set():
                aq, created = AttemptQuestion.objects.get_or_create(attempt=attempt, question=question)
                aq.is_correct = True
            else:
                aq, created = AttemptQuestion.objects.get_or_create(attempt=attempt, question=question)
                aq.is_correct = False
            aq.save()
            aq.given_answers.set(answers[question.id])
            aq.correct_answers.set(correct_answers)
            attempt.status = Attempt.AttemptStatus.ATTEMPTED
            attempt.completed_at = timezone.now()
            attempt.save()
        return HttpResponseRedirect(reverse('quiz:results', args=(quiz.url, attempt.id)))
    return redirect('quiz:quiz_detail', quiz.url)


def results(request, url, attempt_id, **kwargs):
    quiz = get_object_or_404(Quiz, url=url)
    attempt = get_object_or_404(Attempt, id=attempt_id)
    return render(request, "quiz/quiz_results.html", {"quiz": quiz, "attempt": attempt})
