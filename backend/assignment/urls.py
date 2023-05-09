from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path('', views.assignments, name="assignment_list"),
    path('<int:assignment_id>/', views.assignment_details, name="assignment_detail"),
    path('<int:assignment_id>/grade/', views.grade_submissions, name="grade_submissions"),
    path('<int:assignment_id>/<int:user_id>/zip/', views.download_to_zip, name="download_to_zip"),
    path('delete/<int:submission_id>/<int:file_id>', views.delete_file, name="delete_submission"),
    path('delete/<int:submission_id>/', views.bulk_delete_files, name="bulk_delete_files"),
    path('add/', views.add_assignment, name="add_assignment"),
    path('change/<int:pk>/', views.change_assignment, name="change-assignment"),
    path('deleteAssignment/<int:pk>/', views.delete_assignment, name="delete-assignment"),
    path('getAssignemnts/', views.get_assignments_with_form, name="get_assignments"),
]
htmx_urlpatterns = [
    path('htmx/changeAssignment/<int:pk>/', views.htmx_change_assignment, name="htmx-change-assignment"),
]

urlpatterns += htmx_urlpatterns