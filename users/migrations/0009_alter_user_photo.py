# Generated by Django 3.2.13 on 2022-05-05 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_follow_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='uploads/users/user_default.png', null=True, upload_to='uploads/users/', verbose_name='Фото'),
        ),
    ]