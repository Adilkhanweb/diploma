from django.contrib import admin

from course.models import Lesson


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = ("title", "type")
    search_fields = ("title",)
