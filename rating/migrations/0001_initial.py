# Generated by Django 3.2.13 on 2022-05-21 16:57

from django.db import migrations, models
import rating.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.CharField(choices=[('0', '-'), ('1', '*'), ('2', '**'), ('3', '***'), ('4', '****'), ('5', '*****')], default=0, max_length=1, verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
            managers=[
                ('manager', rating.managers.RatingManager()),
            ],
        ),
    ]
