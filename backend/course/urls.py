from django.urls import path

from course import views

urlpatterns = [
    path('<int:assignment_id>', views.assignment_details, name="assignment_detail"),
    path('delete/<int:submission_id>', views.delete_file, name="delete_submission"),
    path('', views.assignments),
]
