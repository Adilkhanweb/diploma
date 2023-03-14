from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from quiz_apps.multiplechoice.models import AttemptQuestion, Attempt
from quiz_apps.quiz.models import Quiz


@receiver(pre_save, sender=Attempt)
def check_attempt(sender, instance, *args, **kwargs):
    attempt = instance
    attempt_questions = AttemptQuestion.objects.filter(attempt=attempt, is_correct=True)
    for question in attempt_questions.all():
        attempt.found_questions.add(question.question)
    try:
        attempt.percentage = attempt_questions.count() * 100 // AttemptQuestion.objects.filter(attempt=attempt).count()
        print(attempt.percentage)
        if attempt.quiz.pass_mark <= attempt.percentage:
            attempt.is_passed = True
    except:
        pass
# @receiver(post_save, sender=Quiz)
# def add_to_events(sender, instance, *args, **kwargs):
#
