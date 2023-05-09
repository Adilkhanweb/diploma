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
        event, created = Event.objects.get_or_create(assignment=instance, url=reverse('assignments:assignment_detail',
                                                                                      kwargs={
                                                                                          'assignment_id': instance.id}))


@receiver(post_save, sender=Quiz)
def create_quiz_event(sender, instance, created, **kwargs):
    if not instance.draft:
        Event.objects.get_or_create(quiz=instance,
                                    url=reverse('quiz:quiz_detail', kwargs={'url': instance.url}))
