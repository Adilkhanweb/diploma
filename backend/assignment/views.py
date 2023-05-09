import datetime
import io
import os
import zipfile

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from diploma_backend.utils import is_teacher_or_moderator
from problems.models import Submission
from users.models import User
# Create your views here.

from .models import Assignment, AssignmentSubmission, AssignmentSubmissionFiles
from .forms import AssignmentForm, AssignmentSubmissionForm, FileSubmissionForm, AssigmentSubmissionForm
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def assignment_details(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    AssignmentSubmissionFormSet = inlineformset_factory(Assignment, AssignmentSubmission, form=AssigmentSubmissionForm,
                                                        extra=0, can_delete=False)
    user = request.user
    submission = AssignmentSubmission.objects.filter(assignment=assignment, user=user).last()
    if request.method == 'POST':
        formset = AssignmentSubmissionFormSet(request.POST, instance=assignment)
        submission, created = AssignmentSubmission.objects.get_or_create(assignment=assignment, user=user)
        submission_form = AssignmentSubmissionForm(request.POST, instance=submission)
        file_form = FileSubmissionForm(request.POST, request.FILES)
        if submission_form.is_valid() and file_form.is_valid():
            submission_f = submission_form.save(commit=False)
            submission_f.save()
            for each in file_form.cleaned_data['files']:
                AssignmentSubmissionFiles.objects.create(file=each, assignment_submission=submission)
        if formset.is_valid():
            for form in formset.forms:
                obj = form.save(commit=False)
                obj.graded = True
                obj.save()
        return render(request, "assignment/partials/assignment-submit-body.html",
                      {'assignment': assignment, 'submission': submission,
                       'submission_form': submission_form, 'file_form': file_form})
    else:
        submission_form = AssignmentSubmissionForm(instance=submission)
        file_form = FileSubmissionForm()
        formset = AssignmentSubmissionFormSet(instance=assignment)

    return render(request, 'assignment/assignment_details.html',
                  {'submission_form': submission_form, 'file_form': file_form, 'assignment': assignment,
                   'submission': submission, 'formset': formset})


def grade_submissions(request, assignment_id):
    """
    Grading submissions of students for assignment
    """
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    AssignmentSubmissionFormSet = inlineformset_factory(Assignment, AssignmentSubmission, form=AssigmentSubmissionForm,
                                                        extra=0, can_delete=False)
    if request.method == 'POST':
        formset = AssignmentSubmissionFormSet(request.POST, instance=assignment)
        if formset.is_valid():
            for form in formset.forms:
                obj = form.save(commit=False)
                obj.graded = True
                obj.save()
            return redirect('assignments:assignment_detail', assignment_id=assignment_id)
        return render(request, 'assignment/assignment_details.html',
                      {'assignment': assignment, 'formset': formset})


@login_required
def assignments(request):
    assignments = Assignment.objects.all()

    q = request.GET.get('q', None)
    if q is not None:
        assignments = assignments.filter(title__istartswith=q)
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
    return redirect('assignments:assignment_detail', assignment.id, submission.user.id)


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
@user_passes_test(is_teacher_or_moderator, login_url='users:signin')
def htmx_change_assignment(request, pk):
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


def change_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.add_message(request, *(messages.SUCCESS, "Өзгерістер Сақталды!"))
        return redirect('assignments:assignment_detail', assignment.id)
    else:
        form = AssignmentForm(instance=assignment)
        return render(request, "assignment/change-assignment.html",
                      {'form': form, 'assignment': assignment})


def bulk_delete_files(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)
    if request.method == 'POST':
        files = request.POST.getlist('bulk_file')
        AssignmentSubmissionFiles.objects.filter(id__in=files).delete()
    return render(request, "assignment/partials/assignment-submissions-tbody.html",
                  {'assignment': submission.assignment, 'submission': submission,
                   'form': AssignmentSubmissionForm(instance=submission)})


def download_to_zip(request, assignment_id, user_id):
    files = []
    user = User.objects.get(id=user_id)
    assignment = Assignment.objects.get(id=assignment_id)
    filename = assignment.title + "_" + user.first_name + "_" + user.last_name + "_attachments.zip"
    buffer = io.BytesIO()

    assignment_submission = AssignmentSubmission.objects.get(assignment=assignment, user__id=user_id)
    with zipfile.ZipFile(buffer, "w") as zip_file:
        for file in assignment_submission.files.all():
            file_path = file.file.path
            zip_file.write(file_path, os.path.basename(file_path))
    response = HttpResponse(buffer.getvalue(), content_type="application/x-zip-compressed")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
