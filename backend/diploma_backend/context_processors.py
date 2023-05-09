from datetime import datetime

from calendarapp.models import Event
from diploma_backend.forms import SearchForm


def all_events(request):
    events = Event.objects.get_all_events()
    running_events = Event.objects.get_running_events()
    search_form = SearchForm()
    page = request.GET.get('page', None)
    q = request.GET.get('q', None)
    if page is not None and q is not None:
        search_form = SearchForm(initial={"page": page, "q": q})
    event_list = []
    # for event in events:
    #     if not event.start_time:
    #         event_list.append({
    #             "title": event.title,
    #             "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #             "url": event.url,
    #         })
    #     elif event.url:
    #         event_list.append({
    #             "title": event.title,
    #             "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #             "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #             "url": event.url,
    #         })
    #     else:
    #         event_list.append(
    #             {
    #                 "title": event.title,
    #                 "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #                 "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    #             }
    #         )
    return {"all_events": event_list, "events_obj": events, 'running_events': running_events,
            "search_form": search_form}
