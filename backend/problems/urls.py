from django.urls import path
from . import views

app_name = "problems"
urlpatterns = [
    path('', views.index, name="problems"),
    path('<slug:slug>/', views.problem_detail, name="problem-detail"),
    path('<slug:slug>/submit/', views.submit, name="submit"),
    path('<slug:slug>/tests/', views.run_tests, name="run_tests"),
    path('<slug:slug>/test/', views.test, name="test"),
]
