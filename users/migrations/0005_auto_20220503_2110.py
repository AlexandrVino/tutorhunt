# Generated by Django 3.2.13 on 2022-05-03 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220503_2108'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='bunch',
            name='unique_bunch',
        ),
        migrations.AddConstraint(
            model_name='bunch',
            constraint=models.UniqueConstraint(condition=models.Q(('status__in', [1, 2])), fields=('teacher', 'student'), name='unique_bunch'),
        ),
    ]