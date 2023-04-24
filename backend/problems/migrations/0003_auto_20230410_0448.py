# Generated by Django 3.2.10 on 2023-04-09 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_submission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='base_code',
            field=models.TextField(blank=True, null=True, verbose_name='Бастапқы берілген код'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.TextField(max_length=1000, null=True, verbose_name='Сипаттама'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 'Оңай'), (2, 'Орташа'), (3, 'Қиын')], default=1, max_length=128, verbose_name='Қиындығы'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='ex_description',
            field=models.TextField(max_length=1000, null=True, verbose_name='Мысал түсіндірмесі'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='ex_input',
            field=models.TextField(max_length=1000, null=True, verbose_name='Кіріс дерегі мысалы'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='ex_output',
            field=models.TextField(max_length=1000, null=True, verbose_name='Шығу мысалы'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='points',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Балл'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Сілтемесі'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_limit',
            field=models.FloatField(default=3, help_text='Кодты орындауға кететін уақыт (секундпен)', verbose_name='Уақыт шегі'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Атауы'),
        ),
    ]