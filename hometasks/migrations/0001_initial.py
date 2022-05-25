# Generated by Django 3.2.13 on 2022-05-21 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hometasks.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hometask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Задание')),
                ('description', models.TextField(help_text='Введите текст домашнего задания', verbose_name='Описание')),
                ('files', models.FileField(null=True, upload_to='uploads/hometasks', verbose_name='Файл')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_hometask', to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Домашнее задание',
                'verbose_name_plural': 'Домашние задания',
            },
            managers=[
                ('manager', hometasks.managers.HometaskManager()),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Выполнено')),
                ('hometask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hometask', to='hometasks.hometask', verbose_name='Домашнее задание')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_hometask', to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Назначение',
                'verbose_name_plural': 'Назначения',
            },
            managers=[
                ('manager', hometasks.managers.AssignmentManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='assignment',
            constraint=models.UniqueConstraint(fields=('student', 'hometask'), name='unique_assignment'),
        ),
    ]
