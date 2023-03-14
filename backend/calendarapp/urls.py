from django.urls import path

from . import views

app_name = "calendarapp"

urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
]