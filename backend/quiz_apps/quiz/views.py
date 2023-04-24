from email._header_value_parser import ContentType

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from quiz_apps.multiplechoice.models import Attempt, AttemptQuestion, Answer, MultipleChoice
from quiz_apps.quiz.forms import AttemptQuestionForm, QuizForm, ChoiceQuestionForm, MultipleChoiceQuestionForm, \
    MAnswerInlineFormset
from quiz_apps.quiz.models import Quiz, BaseQuestion
from django.shortcuts import render

from quiz_apps.quiz.utils import check_attempts, get_score, is_correct
from django.forms import inlineformset_factory

from quiz_apps.singlechoice.admin import SingleCorrectAnswerInlineFormset
from quiz_apps.singlechoice.models import Choice


# from formtools.wizard.views import SessionWizardView

@login_required
def save_question(request, url, id):
    attemptQuestion = AttemptQuestion.objects.get(id=id)
    if request.method == 'POST':
        given_answers = list(map(int, request.POST.getlist(f"{attemptQuestion.id}-given_answers")))
        attemptQuestion.given_answers.set(given_answers)
        correct_answers = list(attemptQuestion.question.answers.filter(correct=True).values_list('id', flat=True))
        # if we have all correct answers and no one incorrect
        if is_correct(given_answers, correct_answers):
            attemptQuestion.is_correct = True
            attemptQuestion.score = get_score(correct_answers, given_answers, attemptQuestion.question)
        else:
            attemptQuestion.is_correct = False
            attemptQuestion.score = get_score(correct_answers, given_answers, attemptQuestion.question)
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
    # quizzes = Quiz.objects.filter(draft=False, end_time__gt=timezone.now())
    quizzes = Quiz.objects.all()
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz_list')
        else:
            return render(request, 'quiz/partials/quiz-add-form.html', {'form': form})
    else:
        form = QuizForm()
        return render(request, "quiz/quiz_list.html", {
            "quizzes": quizzes,
            "form": form
        })


@login_required
def change_quiz(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz_detail', quiz.url)
    form = QuizForm(instance=quiz)
    return render(request, "quiz/partials/quiz-change-form.html", {'form': form, 'quiz': quiz})


@login_required
def delete_quiz(request, url):
    quiz = get_object_or_404(Quiz, url=url)
    quiz.delete()
    quizzes = Quiz.objects.filter(draft=False)
    return render(request, "quiz/partials/quizzes-tbody.html", {'quizzes': quizzes})


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
                 "attempt_question_id": attemptQuestion.id, "question": attemptQuestion.question.content,
                 "figure": (attemptQuestion.question.figure or None)})
        return render(request, 'quiz/attempt.html',
                      {'quiz': quiz, 'forms': forms, 'attempt': attempt, "page_obj": page_obj,
                       "quiz_end_time": quiz_end_time})
    else:
        return redirect('quiz:quiz_detail', quiz.url)


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


@login_required
def results(request, url, attempt_id, **kwargs):
    quiz = get_object_or_404(Quiz, url=url)
    attempt = get_object_or_404(Attempt, id=attempt_id)
    return render(request, "quiz/quiz_results.html", {"quiz": quiz, "attempt": attempt})


@login_required
def add_single_question(request):
    choiceForm = ChoiceQuestionForm()
    ChoiceFormSet = inlineformset_factory(Choice, Answer, fields=('content', 'correct'),
                                          formset=SingleCorrectAnswerInlineFormset, max_num=4, min_num=4, extra=0,
                                          can_delete=False)
    if request.method == 'POST':
        choiceFormSet = ChoiceFormSet(request.POST)
        choiceForm = ChoiceQuestionForm(request.POST, request.FILES)
        if choiceForm.is_valid() and choiceFormSet.is_valid():
            with transaction.atomic():
                choiceQuestion = choiceForm.save()
                choiceFormSet.instance = choiceQuestion
                choiceFormSet.save()
            return redirect('quiz:add-single-question')
        else:
            print(choiceForm.errors)
            print(choiceFormSet.errors)
            return render(request, 'quiz/add_question.html', {'choiceForm': choiceForm, 'choiceFormSet': choiceFormSet})
    return render(request, "quiz/add_question.html",
                  {
                      "choiceForm": ChoiceQuestionForm(),
                      "choiceFormSet": ChoiceFormSet
                  })


@login_required
def add_multiple_question(request):
    multipleChoiceForm = MultipleChoiceQuestionForm()
    MChoiceFormSet = inlineformset_factory(MultipleChoice, Answer, fields=('content', 'correct'),
                                           formset=MAnswerInlineFormset,
                                           max_num=6,
                                           min_num=6,
                                           can_delete=False,
                                           extra=0)

    if request.method == 'POST':
        multipleChoiceFormSet = MChoiceFormSet(request.POST)
        multipleChoiceForm = MultipleChoiceQuestionForm(request.POST, request.FILES)
        if multipleChoiceForm.is_valid() and multipleChoiceFormSet.is_valid():
            with transaction.atomic():
                multipleChoiceQuestion = multipleChoiceForm.save()
                multipleChoiceFormSet.instance = multipleChoiceQuestion
                multipleChoiceFormSet.save()
        return redirect('quiz:add-multiple-question')
    return render(request, "quiz/add_question.html",
                  {
                      "multipleChoiceForm": MultipleChoiceQuestionForm(),
                      'm_choiceformset': MChoiceFormSet
                  })


@login_required
def question_list(request):
    choice_questions = Choice.objects.all()
    multiple_choice_questions = MultipleChoice.objects.all()
    return render(request, "quiz/questions-list.html",
                  {'choice_questions': choice_questions, 'multiple_choice_questions': multiple_choice_questions})


@login_required
def change_multiple_choice_question(request, id):
    question = get_object_or_404(BaseQuestion, id=id)
    if question.answers.count() > 4:
        form = MultipleChoiceQuestionForm(instance=question)
        MChoiceFormSet = inlineformset_factory(MultipleChoice, Answer, fields=('content', 'correct'),
                                               formset=MAnswerInlineFormset,
                                               max_num=6,
                                               min_num=6,
                                               can_delete=False,
                                               extra=0)
        formset = MChoiceFormSet(instance=question)
        if request.method == 'POST':
            form = MultipleChoiceQuestionForm(request.POST, request.FILES, instance=question)
            formset = MChoiceFormSet(request.POST, instance=question)
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                return redirect('quiz:questions_list')
    else:

        form = ChoiceQuestionForm(instance=question)
        ChoiceFormSet = inlineformset_factory(Choice, Answer, fields=('content', 'correct'),
                                              formset=MAnswerInlineFormset,
                                              max_num=4,
                                              min_num=4,
                                              can_delete=False,
                                              extra=0)
        formset = ChoiceFormSet(instance=question)
        if request.method == 'POST':
            form = ChoiceQuestionForm(request.POST, request.FILES, instance=question)
            formset = ChoiceFormSet(request.POST, instance=question)
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                return redirect('quiz:questions_list')
    return render(request, "quiz/multiple-choice-question-change.html",
                  {'form': form, 'formset': formset, 'question': question})
