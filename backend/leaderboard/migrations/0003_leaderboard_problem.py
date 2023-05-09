# Generated by Django 3.2.10 on 2023-05-08 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20230410_1011'),
        ('leaderboard', '0002_leaderboard_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboard',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaderboard_of_this_problem', to='problems.problem'),
        ),
    ]
