from django.contrib import admin
from calendarapp import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        "__str__",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = models.EventMember
    list_display = ["event", "created_at", "updated_at"]
    list_filter = ["event"]


@admin.register(models.RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    model = models.RecurringEvent

    list_display = [
        "title",
        "url",
        "start_date",
        "end_date",
        "days_of_week",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
