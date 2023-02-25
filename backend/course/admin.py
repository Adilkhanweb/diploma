from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from course.models import Lesson, AssignmentSubmission, Assignment

from django.contrib import admin


class CourseAdmin(ModelAdmin):
    """Course Admin."""
    model = Lesson
    menu_label = _("Lesson")
    menu_icon = "media"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ("title",)
    search_fields = ("title",)


admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)

modeladmin_register(CourseAdmin)
