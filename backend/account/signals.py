from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Student, Teacher
from account.models import Profile


@receiver(post_save, sender=Student)
@receiver(post_save, sender=Teacher)
def crete_profile(sender, instance, created, **kwargs):
    """Create profile when user signs up"""
    if created:
        profile = Profile(user=instance)
        profile.save()
