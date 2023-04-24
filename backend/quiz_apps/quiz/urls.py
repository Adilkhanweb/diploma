try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url
from django.urls import path
from quiz_apps.quiz.views import *

app_name = "quiz"
urlpatterns = [
    path('', quiz_list, name="quiz_list"),
    path('questions/', question_list, name="questions_list"),
    path('questions/<int:id>/change/', change_multiple_choice_question, name="change_multiple_choice_question"),
    path('change/<slug:url>/', change_quiz, name="quiz_change"),
    path('delete/<slug:url>/', delete_quiz, name="delete-quiz"),
    path('add-question/single/', add_single_question, name="add-single-question"),
    path('add-question/multiple/', add_multiple_question, name="add-multiple-question"),
    path('<slug:url>/', quiz_detail, name="quiz_detail"),
    path('<slug:url>/attempt/', attempt, name="attempt"),
    path('<slug:url>/submit/', submit, name="submit"),
    path('<slug:url>/<int:id>/save/', save_question, name="save"),
    path('<slug:url>/results/<int:attempt_id>/', results, name="results"),
    path('<slug:url>/<int:attempt_id>/submit_attempt/', submit_attempt, name="submit_attempt"),
]
