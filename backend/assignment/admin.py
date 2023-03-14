from django.contrib import admin

from assignment.models import Assignment, AssignmentSubmission

# Register your models here.
admin.site.register([Assignment, AssignmentSubmission])
