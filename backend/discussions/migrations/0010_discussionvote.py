# Generated by Django 3.2.10 on 2023-04-07 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussions', '0009_alter_discussion_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscussionVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.CharField(choices=[('up', 'Upvote'), ('down', 'Downvote')], max_length=4)),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discussions.discussion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]