# Generated by Django 3.2.10 on 2023-04-09 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0008_alter_assignmentsubmission_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submissions', to='assignment.assignment', verbose_name='Тапсырма атауы'),
        ),
    ]