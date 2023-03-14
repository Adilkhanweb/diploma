from calendarapp.models import Event


def all_events(request):
    events = Event.objects.get_all_events()
    event_list = []
    for event in events:
        if not event.start_time:
            event_list.append({
                "title": event.title,
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "url": event.url,
            })
        elif event.url:
            event_list.append({
                "title": event.title,
                "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "url": event.url,
            })
        else:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
    return {"all_events": event_list}
