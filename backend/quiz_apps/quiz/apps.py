from django.apps import AppConfig


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz_apps.quiz'

    def ready(self):
        import quiz_apps.quiz.signals
