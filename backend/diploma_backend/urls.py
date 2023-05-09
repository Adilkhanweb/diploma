from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from diploma_backend.views import *

app_name = "core"
urlpatterns = [
    path("", main_page, name="main_page"),
    path("q/", searchbar, name="searchbar"),
    path("create-user/", create_user, name="create-user"),
    path("users/", user_list, name="users"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("addbook/", addBook, name="addbook"),
    path("addlesson/", addLesson, name="addlesson"),
    path("updatelesson/<int:pk>/", update_lesson, name="update-lesson"),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('quiz/', include('quiz_apps.quiz.urls')),
    path("", include("calendarapp.urls")),
    path("problems/", include("problems.urls")),
    path("assignments/", include("assignment.urls")),
    path('socialaccount/', include('allauth.urls')),

    path('discussions/', include('discussions.urls')),

    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]
htmx_urlpatterns = [
    path("lessons/", lessons_list, name="get_lessons"),
    path("books/", books_list, name="get_books"),
    path("delete_lesson/<int:pk>", delete_lesson, name="delete_lesson"),
]
urlpatterns += htmx_urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = handler404
handler500 = handler500
