from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from problems.models import Problem, TestCase


#

@receiver(pre_save, sender=Problem)
def count_testcases(sender, instance, *args, **kwargs):
    problem = instance
    problem.testcases_count = problem.testcases.count()

#
#
# @receiver(post_save, sender=TestCase)
# def count_testcases(sender, instance, *args, **kwargs):
#     testcase = instance
#     testcase.problem.testcases_count = testcase.problem.testcases.count()
