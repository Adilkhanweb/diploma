from django.shortcuts import render
import judge0api as api

from .models import *
from django.conf import settings

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
    return render(request, "problems/problems-list.html", {'problems': problems})


def problem_detail(request, slug):
    problem = Problem.objects.get(slug=slug)
    return render(request, "problems/problem-detail.html", {'problem': problem,
                                                            'is_accepted': problem.submission_set.filter(
                                                                user=request.user, is_accepted=True).exists()})


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
                38,
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
                38,
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
        print(testcase_statuses)
        return render(request, "problems/problem-detail.html",
                      {'problem': problem, 'statuses': testcase_statuses, 'code': code})
    return render(request, "problems/problem-detail.html", {'problem': problem})


def test(request, slug):
    problem = Problem.objects.get(slug=slug)
    client = api.Client(settings.JUDGE0_API_URL)
    client.wait = True
    if request.method == 'POST':
        code = request.POST.get('code')
        test_input = request.POST.get('test')
        submission = api.submission.submit(
            client,
            bytes(code, "utf-8"),
            38,
            stdin=bytes(test_input, "utf-8"))
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
