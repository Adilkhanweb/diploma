try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url
from django.urls import path
from quiz.views import QuizListView, CategoriesListView, \
    ViewQuizListByCategory, QuizUserProgressView, QuizMarkingList, \
    QuizMarkingDetail, QuizDetailView, QuizTake

urlpatterns = [

    path('',
         QuizListView.as_view(),
         name='quiz_index'),

    path('category/',
         CategoriesListView.as_view(),
         name='quiz_category_list_all'),

    path('category/<str:category_name>/',
         ViewQuizListByCategory.as_view(),
         name='quiz_category_list_matching'),

    path('progress/', QuizUserProgressView.as_view(),
         name='quiz_progress'),

    path('marking/',
         QuizMarkingList.as_view(),
         name='quiz_marking'),

    path('marking/<int:pk>',
         QuizMarkingDetail.as_view(),
         name='quiz_marking_detail'),

    #  passes variable 'quiz_name' to quiz_take view
    path('<slug:slug>/',
         QuizDetailView.as_view(),
         name='quiz_start_page'),

    path('<str:quiz_name>/take/',
         QuizTake.as_view(),
         name='quiz_question'),
]
