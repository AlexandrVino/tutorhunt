# Generated by Django 3.2.13 on 2022-05-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_notificationmodel_initiator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationmodel',
            name='category',
            field=models.CharField(choices=[('подписки', 'подписки')], max_length=20, verbose_name='категория'),
        ),
    ]
