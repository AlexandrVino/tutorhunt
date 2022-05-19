# Generated by Django 3.2.13 on 2022-05-19 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='initiator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='caused_notifications', to=settings.AUTH_USER_MODEL, verbose_name='отправитель'),
        ),
        migrations.AddField(
            model_name='notificationmodel',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL, verbose_name='получатель'),
        ),
    ]