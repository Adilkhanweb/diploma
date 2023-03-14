from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from assignment.models import Assignment
from calendarapp.models import Event
from quiz_apps.quiz.models import Quiz


@receiver(post_save, sender=Assignment)
def create_event(sender, instance, created, **kwargs):
    """Create event when assignment will be created"""
    if created:
        event = Event.objects.create(title=instance.title, start_time=instance.created_at, end_time=instance.deadline,
                                     url=reverse('assignments:assignment_detail',
                                                 kwargs={'assignment_id': instance.id}))


@receiver(post_save, sender=Quiz)
def create_quiz_event(sender, instance, created, **kwargs):
    if created and not instance.draft:
        event = Event.objects.create(title=instance.title, start_time=instance.start_time, end_time=instance.end_time,
                                     url=reverse('quiz:quiz_detail', kwargs={'url': instance.url}))
