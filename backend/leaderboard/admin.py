from django.contrib import admin

from leaderboard.models import Leaderboard


# Register your models here.
@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score',)
    list_filter = ('user', 'quiz',)

    class Meta:
        model = Leaderboard
