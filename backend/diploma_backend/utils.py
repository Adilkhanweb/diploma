
def is_teacher_or_moderator(user):
    return user.groups.filter(name__in=['Teachers', 'Moderators']).exists() or user.is_superuser

