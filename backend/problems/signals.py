from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from leaderboard.models import Leaderboard
from problems.models import Problem, TestCase, Submission


#

@receiver(pre_save, sender=Problem)
def count_testcases(sender, instance, *args, **kwargs):
    problem = instance
    problem.testcases_count = problem.testcases.count()


@receiver(post_save, sender=Submission)
def create_or_update_leaderboard(sender, instance, *args, **kwargs):
    submission = instance
    leaderboard, created = Leaderboard.objects.get_or_create(user=submission.user, problem=submission.problem)
    if submission.is_accepted:
        leaderboard.score = submission.problem.points
    else:
        leaderboard.score = 0
    leaderboard.save()
