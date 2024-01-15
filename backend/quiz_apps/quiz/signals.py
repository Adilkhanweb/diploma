from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from leaderboard.models import Leaderboard
from quiz_apps.multiplechoice.models import AttemptQuestion, Attempt, MultipleChoice
from quiz_apps.quiz.models import Quiz
from quiz_apps.singlechoice.models import Choice


@receiver(pre_save, sender=Attempt)
def check_attempt(sender, instance, *args, **kwargs):
    attempt = instance
    max_possible_score = attempt.quiz.get_max_scores()
    attempt_score = attempt.get_attempt_score()
    try:
        attempt.percentage = attempt_score * 100 // max_possible_score
        if attempt.quiz.pass_mark <= attempt.percentage:
            attempt.is_passed = True
        else:
            attempt.is_passed = False
    except:
        pass


@receiver(post_save, sender=Attempt)
def create_attempt_questions(sender, instance, *args, **kwargs):
    """Create attempt questions"""
    attempt = instance
    for question in attempt.quiz.questions.all():
        correct_answers = question.answers.filter(correct=True)
        aq, created = AttemptQuestion.objects.get_or_create(attempt=attempt, question=question)
        aq.correct_answers.set(list(correct_answers.values_list('id', flat=True)))
    """Create or update a leaderboard score for the quiz attempted by the user"""
    leaderboard, created = Leaderboard.objects.get_or_create(user=attempt.user, quiz=attempt.quiz)
    leaderboard.score = attempt.get_attempt_score()
    leaderboard.save()


@receiver(pre_save, sender=MultipleChoice)
def update_score(sender, instance, *args, **kwargs):
    """
    update the score of the multiple choice question
    by default the score is 1 for all questions
    """
    mc = instance
    mc.score = 2
    if mc.correct_answers_count == 0:
        mc.correct_answers_count = mc.answers.filter(correct=True).count()
