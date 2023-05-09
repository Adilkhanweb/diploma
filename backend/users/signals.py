from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Student, Teacher
from users.models import Profile
from allauth.account.signals import user_signed_up


@receiver(post_save, sender=Student)
@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=get_user_model())
def crete_profile(sender, instance, created, **kwargs):
    """Create profile when user signs up"""
    if created:
        profile = Profile(user=instance)
        profile.save()


@receiver(user_signed_up)
def add_to_student_group(sender, request, user, **kwargs):
    group, created = Group.objects.get_or_create(name='Students')
    user.groups.add(group)
