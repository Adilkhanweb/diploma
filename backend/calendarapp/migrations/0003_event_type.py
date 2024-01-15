# Generated by Django 3.2.10 on 2023-05-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('lesson', 'Lesson'), ('book', 'Book'), ('quiz', 'Quiz'), ('assignment', 'Assignment'), ('discussion', 'Discussion'), ('problem', 'Problem')], default='', max_length=13),
        ),
    ]