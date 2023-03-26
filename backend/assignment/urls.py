from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path('', views.assignments, name="assignment_list"),
    path('<int:assignment_id>', views.assignment_details, name="assignment_detail"),
    path('delete/<int:submission_id>', views.delete_file, name="delete_submission"),
    path('addAssignment', views.add_assignment, name="add_assignment"),
]
