# Generated by Django 3.2.10 on 2023-04-06 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiplechoice', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Жауап', 'verbose_name_plural': 'Жауаптар'},
        ),
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.CharField(help_text='Көрсеткіңіз келетін жауап мәтінін енгізіңіз', max_length=1000, verbose_name='Жауап'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False, help_text='Бұл дұрыс жауап па?', verbose_name='Дұрыс'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='status',
            field=models.CharField(choices=[('attempted', 'Әрекет жасалды'), ('attempting', 'Әрекет жасалуда'), ('not', 'Әрекет жасалмады')], default='not', max_length=20),
        ),
    ]