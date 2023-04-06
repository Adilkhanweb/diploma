from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path('', views.assignments, name="assignment_list"),
    path('<int:assignment_id>/', views.assignment_details, name="assignment_detail"),
    path('delete/<int:submission_id>/<int:file_id>', views.delete_file, name="delete_submission"),
    path('delete/<int:submission_id>/', views.bulk_delete_files, name="bulk_delete_files"),
    path('addAssignment', views.add_assignment, name="add_assignment"),
    path('deleteAssignment/<int:pk>/', views.delete_assignment, name="delete-assignment"),
    path('changeAssignment/<int:pk>/', views.change_assignment, name="change-assignment"),
    path('getAssignemnts/', views.get_assignments_with_form, name="get_assignments"),
]
