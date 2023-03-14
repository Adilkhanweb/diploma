from django.contrib import admin
from .models import *


# Register your models here.
class TestCaseInline(admin.TabularInline):
    model = TestCase
    fields = ('input', 'expected_output', 'is_hidden')


class ProblemAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]
    prepopulated_fields = {'slug': ('title',)}


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_accepted')
    list_editable = ('is_accepted',)


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem', 'input', 'expected_output', 'is_hidden')
    list_editable = ('is_hidden',)
    list_filter = ('problem', 'is_hidden')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(Submission, SubmissionAdmin)
