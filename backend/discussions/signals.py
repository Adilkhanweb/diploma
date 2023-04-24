from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from discussions.models import Discussion, Reply


@receiver(pre_save, sender=Discussion)
@receiver(pre_save, sender=Reply)
def update_score(sender, instance, *args, **kwargs):
    instance.score = instance.up_votes - instance.down_votes
