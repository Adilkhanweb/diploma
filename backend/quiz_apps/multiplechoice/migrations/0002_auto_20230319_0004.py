# Generated by Django 3.2.10 on 2023-03-18 18:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('multiplechoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptquestion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attemptquestion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
