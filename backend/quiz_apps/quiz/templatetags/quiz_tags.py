import humanize
from django import template
from django.db.models import Q
from humanize import naturaldelta, activate, naturaltime, naturaldate
from django.utils import timezone
from discussions.models import Reply, Discussion
from leaderboard.models import Leaderboard
from problems.models import Submission
from quiz_apps.multiplechoice.models import Attempt
from quiz_apps.quiz.models import Quiz

register = template.Library()


@register.filter
def answer_choice_to_string(question, answer):
    return question.answer_choice_to_string(answer)


@register.filter
def to_char(value):
    return chr(64 + value)


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.filter(name='event_color')
def event_color(end_time):
    today = timezone.now().date()
    days = (end_time.date() - today).days
    if days > 30:
        return generate_hex_color(1)
    else:
        return generate_hex_color(days / 30)


def generate_hex_color(coefficient):
    r = int((1 - coefficient) * 255)
    g = int(coefficient * 255)
    b = 0
    return f"#{r:02x}{g:02x}{b:02x}"


#
#
# @register.filter
# def duration_humanize(duration):
#     """
#         Returns a humanized duration string.
#     """
#     humanize.i18n.activate(locale="kk_KZ", path="quiz_apps/locale/")
#     return naturaldelta(duration, months=False, minimum_unit='seconds')
#
#
# @register.filter
# def naturaltime_humanize(date):
#     humanize.i18n.activate(locale="kk_KZ", path="quiz_apps/locale/")
#     naive = date.replace(tzinfo=None)
#     return naturaltime(value=naive)
#

@register.filter
def problem_is_accepted(problem, user):
    return Submission.objects.filter(problem=problem, user=user, is_accepted=True).exists()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def get_quiz_attempts(quiz_id, user_id):
    return Attempt.objects.filter(quiz_id=quiz_id, status=Attempt.AttemptStatus.ATTEMPTED, user_id=user_id)


@register.filter
def get_quiz_attempts_count(quiz_id, user_id):
    return Attempt.objects.filter(quiz_id=quiz_id, status=Attempt.AttemptStatus.ATTEMPTED, user_id=user_id).count()


@register.filter
def get_leaderboard_ordered(quiz_id, user_id):
    user_score = Leaderboard.objects.filter(quiz_id=quiz_id, user_id=user_id).last()
    return Leaderboard.objects.filter(
        Q(quiz_id=quiz_id, score__gt=user_score.score) | Q(quiz_id=quiz_id, score=user_score.score,
                                                           pk__lt=user_score.pk)).order_by(
        '-score'), user_score, Leaderboard.objects.filter(
        Q(quiz_id=quiz_id, score__lt=user_score.score) | Q(quiz_id=quiz_id, score=user_score.score,
                                                           pk__gt=user_score.pk)).order_by(
        'score')


@register.filter
def make_ordinal_kz(number):
    juan = [6, 9, 10]
    last_digit = abs(number) % 10
    if last_digit in juan:
        return f"{number}-шы"
    else:
        return f"{number}-ші"


@register.filter
def reply_is_upvoted(reply_id, user_id):
    votes = Reply.objects.get(id=reply_id).vote_set.all()
    print(votes)
    print(votes.filter(user__id=user_id, vote_type='up').exists())
    return votes.filter(user__id=user_id, vote_type='up').exists()


@register.filter
def reply_is_downvoted(reply_id, user_id):
    votes = Reply.objects.get(id=reply_id).vote_set.all()
    return votes.filter(user__id=user_id, vote_type='down').exists()


@register.filter
def discussion_is_upvoted(discussion_id, user_id):
    votes = Discussion.objects.get(id=discussion_id).discussionvote_set.all()
    return votes.filter(user_id=user_id, vote_type='up').exists()


@register.filter
def discussion_is_downvoted(discussion_id, user_id):
    votes = Discussion.objects.get(id=discussion_id).discussionvote_set.all()
    return votes.filter(user__id=user_id, vote_type='down').exists()
