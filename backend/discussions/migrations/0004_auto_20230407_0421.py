# Generated by Django 3.2.10 on 2023-04-06 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussions', '0003_remove_discussion_user_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='discussions.discussion')),
                ('down_votes', models.ManyToManyField(related_name='reply_down_votes', to=settings.AUTH_USER_MODEL)),
                ('up_votes', models.ManyToManyField(related_name='reply_up_votes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='discussion',
            name='correct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correct_reply', to='discussions.reply'),
        ),
    ]
