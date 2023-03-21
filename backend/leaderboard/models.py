from django.db import models

from account.models import User
from quiz_apps.quiz.models import Quiz


# Create your models here.
class Leaderboard(models.Model):
    score = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="leaderboard_of_this_quiz"
    )

    def __str__(self):
        return self.user.username + " in " + self.quiz.title

    class Meta:
        ordering = ["-quiz_created_at", "-score"]
