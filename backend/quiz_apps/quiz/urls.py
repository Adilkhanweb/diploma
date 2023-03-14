try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url
from django.urls import path
from quiz_apps.quiz.views import *

app_name = "quiz"
urlpatterns = [
    path('', quiz_list, name="quiz_list"),
    path('<slug:url>/', quiz_detail, name="quiz_detail"),
    path('<slug:url>/attempt/', attempt, name="attempt"),
    path('<slug:url>/submit/', submit, name="submit"),
    path('<slug:url>/results/<int:attempt_id>/', results, name="results"),
]
