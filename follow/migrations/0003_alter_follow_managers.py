# Generated by Django 3.2.13 on 2022-05-23 15:30

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='follow',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
