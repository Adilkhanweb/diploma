from django.db import models

from problems.models import Problem
from users.models import User
from quiz_apps.quiz.models import Quiz


# Create your models here.
class Leaderboard(models.Model):
    score = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="leaderboard_of_this_quiz", null=True, blank=True
    )

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="leaderboard_of_this_problem",
                                null=True, blank=True)

    def __str__(self):
        if self.quiz:
            return self.user.first_name + " in " + self.quiz.title
        else:
            return self.user.first_name + " in " + self.problem.title

    class Meta:
        ordering = ["-score"]
