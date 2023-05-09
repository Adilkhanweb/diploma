# Generated by Django 3.2.10 on 2023-05-08 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0010_auto_20230410_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(verbose_name='Аяқталу мерзімі'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(verbose_name='Сипаттама'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Атауы'),
        ),
    ]
