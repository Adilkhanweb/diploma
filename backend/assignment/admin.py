from django.contrib import admin

from assignment.models import Assignment, AssignmentSubmission, AssignmentSubmissionFiles

# Register your models here.
admin.site.register([Assignment, AssignmentSubmission, AssignmentSubmissionFiles])
