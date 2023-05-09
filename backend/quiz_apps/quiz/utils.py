from django.utils import timezone

from quiz_apps.multiplechoice.models import Attempt


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


def get_score(correct_answers, given_answers, question):
    """
    If correct answers are [A, B, C] and given answers are [A, B, E] (2 correct, 1 incorrect)
    then the score is 2 / 3 * 2 =
    """
    # Создаем множества правильных и даных ответов
    correct_set = set(correct_answers)
    given_set = set(given_answers)
    max_possible_score = 2 if question.answers.count() > 4 else 1
    correct_given = correct_set.intersection(given_set)
    wrong_given = given_set.difference(correct_set)
    if len(wrong_given) >= len(correct_given):
        return 0
    else:
        score = len(correct_given) / len(correct_set) * max_possible_score
        return int(score)
