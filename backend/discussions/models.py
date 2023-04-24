from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

from users.models import User


class Discussion(models.Model):
    class Status(models.TextChoices):
        ANSWERED = 'answered', 'Жауап берілді'
        NOT_ANSWERED = 'not_answered', 'Жауап берілмеді'

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = CKEditor5Field(config_name="default")
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    correct = models.ForeignKey('discussions.Reply', on_delete=models.CASCADE, related_name="correct_reply", blank=True,
                                null=True)
    score = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)
    status = models.CharField(verbose_name="Күйі", choices=Status.choices, default=Status.NOT_ANSWERED, max_length=20)
    user_lst = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def sum_visits(self, user_id=None):
        if user_id:
            if self.user_lst:
                lst = self.user_lst.split(',')
                if str(user_id) not in lst:
                    self.user_lst += ',' + str(user_id)
                    self.visits += 1
            else:
                self.user_lst = str(user_id)
        self.save()

    def has_seen(self, user=None):
        if user.is_authenticated():
            if self.user_lst:
                lst = self.user_lst.split(',')
                if str(user.id) in lst:
                    return True
            return False
        return True


class DiscussionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey('Discussion', on_delete=models.CASCADE)
    vote_type = models.CharField(choices=(('up', 'Upvote'), ('down', 'Downvote')), max_length=4)


class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="replies")
    description = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}: {self.discussion.title}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE)
    vote_type = models.CharField(choices=(('up', 'Upvote'), ('down', 'Downvote')), max_length=4)
