import datetime

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from .models import Assignment, AssignmentSubmission
from .forms import AssignmentSubmissionForm
from django.contrib.auth.decorators import login_required


@login_required
def assignment_details(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment).filter(user=request.user)
    if request.method == "POST":
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            for f in files:
                file_instance = AssignmentSubmission(files=f, user=request.user, assignment=assignment)
                file_instance.save()
    return render(request, "assignment/assignment_details.html", {
        "form": AssignmentSubmissionForm(initial={'assignment': assignment, 'user': request.user}),
        "submissions": submissions,
        "assignment": assignment
    })


def assignments(request):
    assignments = Assignment.objects.filter(deadline__gt=datetime.datetime.now())
    context = {
        "assignments": assignments
    }

    return render(request, "assignment/assignment_list.html", context)


def delete_file(request, submission_id):
    file = AssignmentSubmission.objects.get(id=submission_id)
    assignment = file.assignment
    file.delete()
    return redirect('assignments:assignment_detail', assignment.id)
