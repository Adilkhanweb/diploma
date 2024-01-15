from typing import List

from django.utils import timezone

from quiz_apps.multiplechoice.models import Attempt
from quiz_apps.quiz.models import BaseQuestion


def check_attempts(quiz, user):
    if Attempt.objects.filter(quiz=quiz, user=user, status=Attempt.AttemptStatus.ATTEMPTING).exists():
        attempt = Attempt.objects.filter(quiz=quiz, user=user, status=Attempt.AttemptStatus.ATTEMPTING).last()
        remaining_time = attempt.created_at + quiz.duration - timezone.now()
        # if remaining time 10 seconds set attempt as attempted
        if remaining_time.total_seconds() < 1:
            attempt.status = Attempt.AttemptStatus.ATTEMPTED
            attempt.save()
    return (quiz.start_time <= timezone.now() <= quiz.end_time) and \
        Attempt.objects.filter(quiz=quiz, user=user, status=Attempt.AttemptStatus.ATTEMPTED).count() < quiz.max_attempts


def is_correct(correct_answers, given_answers):
    """ Checks whether the given answers are correct"""
    return set(correct_answers).intersection(set(given_answers)) == set(correct_answers) and set(
        given_answers).difference(set(correct_answers)) == set()


def get_score(correct_answers: List[int], given_answers: List[int], question: BaseQuestion) -> int:
    correct_set = set(correct_answers)  # Correct answers
    given_set = set(given_answers)  # User answers
    max_possible_score = question.score  # Max possible score
    correct_given = correct_set.intersection(given_set)  # User correct answers
    wrong_given = given_set.difference(correct_set)  # User incorrect answers
    if len(wrong_given) >= len(correct_given):  # if user correct answers less than incorrect answers, score will be 0
        return 0
    else:
        score = len(correct_given) / len(correct_set) * max_possible_score  # else score will be calculated
        return int(score)

