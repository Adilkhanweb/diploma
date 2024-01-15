from django.shortcuts import render, redirect, get_object_or_404
import judge0api as api

from .forms import ProblemForm, TestCaseForm
from .models import *
from django.conf import settings
from django.forms import inlineformset_factory
from django.db import transaction
from django.utils.safestring import mark_safe

STATUSES = [
    {
        "id": 1,
        "description": "Кезекте"
    },
    {
        "id": 2,
        "description": "Өңдеу"
    },
    {
        "id": 3,
        "description": "Қабылданды"
    },
    {
        "id": 4,
        "description": "Қате жауап"
    },
    {
        "id": 5,
        "description": "Уақыт шегінен асып кетті"
    },
    {
        "id": 6,
        "description": "Компиляция қатесі"
    },
    {
        "id": 7,
        "description": "Жұмыс уақыты қатесі (SIGSEGV)"
    },
    {
        "id": 8,
        "description": "Жұмыс уақыты қатесі (SIGXFSZ)"
    },
    {
        "id": 9,
        "description": "Жұмыс уақыты қатесі (SIGFPE)"
    },
    {
        "id": 10,
        "description": "Жұмыс уақыты қатесі (SIGABRT)"
    },
    {
        "id": 11,
        "description": "Жұмыс уақыты қатесі (NZEC)"
    },
    {
        "id": 12,
        "description": "Жұмыс уақытындағы қате (басқа)"
    },
    {
        "id": 13,
        "description": "Ішкі қате"
    },
    {
        "id": 14,
        "description": "Орындау пішімі қатесі"
    }
]


# Create your views here.
def index(request):
    problems = Problem.objects.all()

    q = request.GET.get('q', None)
    if q is not None:
        problems = problems.filter(title__istartswith=q)
    return render(request, "problems/problems-list.html", {'problems': problems})


def problem_detail(request, slug):
    problem = Problem.objects.get(slug=slug)
    submissions = Submission.objects.filter(problem=problem, user=request.user)
    return render(request, "problems/problem-detail.html", {'problem': problem,
                                                            'is_accepted': problem.submission_set.filter(
                                                                user=request.user, is_accepted=True).exists(),
                                                            "submissions": submissions})


TestCaseFormSet = inlineformset_factory(Problem, TestCase, form=TestCaseForm, extra=1, can_delete=True)


def add_problem(request):
    form = ProblemForm()
    if request.method == "POST":
        form = ProblemForm(request.POST)
        formset = TestCaseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                problem = form.save()
                formset.instance = problem
                formset.save()
                problem.testcases_count = problem.testcases.count()
                problem.save()
            return redirect('problems:problems')
    return render(request, "problems/add-problem.html", {'form': ProblemForm(), 'formset': TestCaseFormSet})


def change_problem(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    form = ProblemForm(instance=problem)
    formset = TestCaseFormSet(instance=problem)
    if request.method == "POST":
        form = ProblemForm(request.POST, instance=problem)
        formset = TestCaseFormSet(request.POST, instance=problem)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                problem = form.save()
                formset.instance = problem
                formset.save()
                problem.testcases_count = problem.testcases.count()
                problem.save()
            return redirect('problems:problems')
        else:
            return redirect('problems:change-problem')
    return render(request, "problems/change-problem.html",
                  {'form': ProblemForm(instance=problem), 'formset': formset, 'problem': problem})


def submit(request, slug):
    problem = Problem.objects.get(slug=slug)
    client = api.Client(settings.JUDGE0_API_URL)
    client.wait = True
    testcase_statuses = []
    times = []
    memories = []
    success_tc = 0
    if request.method == 'POST':
        code = request.POST.get('code')
        for testcase in problem.testcases.all():
            submission = api.submission.submit(
                client,
                bytes(code, "utf-8"),
                settings.JUDGE0_LANG_ID,
                stdin=bytes(testcase.input, "utf-8"),
                expected_output=bytes(testcase.expected_output, "utf-8"))
            submission.load(client)
            times.append(float(submission.time))
            memories.append(submission.memory)
            success_tc += 1 if submission.status['id'] == 3 else 0
            stdout = ""
            if submission.stdout is not None:
                stdout = submission.stdout.decode("utf-8")
            else:
                stdout = submission.stderr.decode('utf-8')
            if testcase.is_hidden:
                testcase_statuses.append(
                    {"status": next(item for item in STATUSES if item['id'] == submission.status['id']),
                     "output": "Жасырын сынақ мысалы",
                     "expected_output": "Жасырын сынақ мысалы"})
            else:
                testcase_statuses.append(
                    {"status": next(item for item in STATUSES if item['id'] == submission.status['id']),
                     "output": stdout,
                     "expected_output": submission.expected_output.decode('utf-8')})

        is_accepted = True
        for testcase in testcase_statuses:
            if testcase['status']['id'] != 3:
                is_accepted = False
                break
        code_submission = Submission(user=request.user, problem=problem, source_code=code, is_accepted=is_accepted,
                                     avg_time=(sum(times) / len(times)), success_testcases=success_tc,
                                     avg_memory=(sum(memories) / len(memories)))
        code_submission.save()
        return render(request, "problems/problem-detail.html",
                      {'problem': problem, 'statuses': testcase_statuses, 'code': code, })
    return render(request, "problems/problem-detail.html", {'problem': problem})


def run_tests(request, slug):
    problem = Problem.objects.get(slug=slug)
    client = api.Client(settings.JUDGE0_API_URL)
    client.wait = True
    testcase_statuses = []
    if request.method == 'POST':
        code = request.POST.get('code')
        for testcase in problem.testcases.filter(is_hidden=False):
            submission = api.submission.submit(
                client,
                bytes(code, "utf-8"),
                settings.JUDGE0_LANG_ID,
                stdin=bytes(testcase.input, "utf-8"),
                expected_output=bytes(testcase.expected_output, "utf-8"))
            submission.load(client)
            stdout = ""
            if submission.stdout is not None:
                stdout = submission.stdout.decode("utf-8")
            else:
                stdout = submission.stderr.decode('utf-8')
            testcase_statuses.append(
                {"status": next(item for item in STATUSES if item['id'] == submission.status['id']), "output": stdout,
                 "expected_output": submission.expected_output.decode('utf-8')})
        return render(request, "problems/problem-detail.html",
                      {'problem': problem, 'statuses': testcase_statuses, 'code': code})
    return render(request, "problems/problem-detail.html", {'problem': problem})


def test(request, slug):
    problem = Problem.objects.get(slug=slug)
    client = api.Client("http://localhost")
    client.wait = True
    if request.method == 'POST':
        code = request.POST.get('code')
        test_input = request.POST.get('test')
        submission = api.submission.submit(
            client,
            bytes(code, "utf-8"),
            settings.JUDGE0_LANG_ID,
            stdin=bytes(test_input, "utf-8"),
            wall_time_limit=5,)
        submission.load(client)
        stdout = ""
        if submission.stdout is not None:
            stdout = submission.stdout.decode("utf-8")
        else:
            stdout = submission.stderr.decode('utf-8')

        return render(request, "problems/problem-detail.html",
                      {'problem': problem, 'output': stdout, 'code': code,
                       'input': test_input})
    return render(request, "problems/problem-detail.html", {'problem': problem})


def delete_problem(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    problem.delete()
    return render(request, 'problems/partails/problem-list-body.html', {'problems': Problem.objects.all()})
