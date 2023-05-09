# Generated by Django 3.2.10 on 2023-05-07 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0010_auto_20230410_0408'),
        ('quiz', '0006_auto_20230409_1706'),
        ('calendarapp', '0004_alter_event_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='type',
        ),
        migrations.AddField(
            model_name='event',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_events', to='assignment.assignment'),
        ),
        migrations.AddField(
            model_name='event',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_events', to='quiz.quiz'),
        ),
    ]
