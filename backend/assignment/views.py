import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from problems.models import Submission
# Create your views here.

from .models import Assignment, AssignmentSubmission, AssignmentSubmissionFiles
from .forms import AssignmentForm, AssignmentSubmissionForm, FileSubmissionForm
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def assignment_details(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submission = AssignmentSubmission.objects.filter(assignment=assignment, user=request.user).last()
    if request.method == 'POST':
        submission, created = AssignmentSubmission.objects.get_or_create(assignment=assignment, user=request.user)
        submission_form = AssignmentSubmissionForm(request.POST, instance=submission)
        file_from = FileSubmissionForm(request.POST, request.FILES)
        if submission_form.is_valid() and file_from.is_valid():
            submission_f = submission_form.save(commit=False)
            submission_f.save()
            for each in file_from.cleaned_data['files']:
                AssignmentSubmissionFiles.objects.create(file=each, assignment_submission=submission)
            return render(request, "assignment/partials/assignment-submissions-tbody.html",
                          {'assignment': assignment, 'submission': submission,
                           'form': AssignmentSubmissionForm()})
        else:
            print(submission_form.errors)
            print(file_from.errors)
    else:
        submission_form = AssignmentSubmissionForm(instance=submission)
        file_from = FileSubmissionForm()
    return render(request, 'assignment/assignment_details.html',
                  {'submission_form': submission_form, 'file_from': file_from, 'assignment': assignment,
                   'submission': submission})


@login_required
def assignments(request):
    assignments = Assignment.objects.all()
    context = {
        "assignments": assignments,
        "form": AssignmentForm()
    }

    return render(request, "assignment/assignment_list.html", context)


@login_required
def get_assignments_with_form(request):
    assignments = Assignment.objects.all()
    context = {
        "assignments": assignments,
        "form": AssignmentForm()
    }

    return render(request, "assignment/partials/asignments-body.html", context)


def delete_file(request, submission_id, file_id):
    submission = AssignmentSubmission.objects.get(id=submission_id)
    assignment = submission.assignment
    get_object_or_404(AssignmentSubmissionFiles, id=file_id).delete()
    return redirect('assignments:assignment_detail', assignment.id)


def add_assignment(request):
    assignments = Assignment.objects.filter(deadline__gt=datetime.datetime.now())
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            return render(request, "assignment/partials/asignments-body.html",
                          {"form": AssignmentForm(), 'assignments': assignments})
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)


def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.delete()
    assignments = Assignment.objects.filter(deadline__gt=datetime.datetime.now())
    return render(request, "assignment/partials/assinments-list.html", {'assignments': assignments})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Teacher').count() == 0, login_url='users:signin')
def change_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    assignments = Assignment.objects.filter(deadline__gt=datetime.datetime.now())
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
        return render(request, "assignment/partials/asignments-body.html",
                      {"form": AssignmentForm(), 'assignments': assignments})
    else:
        form = AssignmentForm(instance=assignment)
        return render(request, "assignment/partials/assignment-change-form.html",
                      {'form': form, 'assignment': assignment})


def bulk_delete_files(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)
    if request.method == 'POST':
        files = request.POST.getlist('bulk_file')
        AssignmentSubmissionFiles.objects.filter(id__in=files).delete()
    return render(request, "assignment/partials/assignment-submissions-tbody.html",
                  {'assignment': submission.assignment, 'submission': submission,
                   'form': AssignmentSubmissionForm(instance=submission)})
