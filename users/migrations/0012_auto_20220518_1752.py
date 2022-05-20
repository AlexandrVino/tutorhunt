# Generated by Django 3.2.13 on 2022-05-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_user_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bunch',
            options={'ordering': ('datetime',), 'verbose_name': 'Связка', 'verbose_name_plural': 'Связки'},
        ),
        migrations.RemoveConstraint(
            model_name='bunch',
            name='unique_bunch',
        ),
        migrations.AddField(
            model_name='bunch',
            name='datetime',
            field=models.CharField(default=None, max_length=10, verbose_name='Время занятия'),
        ),
        migrations.AlterField(
            model_name='bunch',
            name='status',
            field=models.CharField(choices=[('Waiting', 'Waiting'), ('Accepted', 'Accepted'), ('Finished', 'Finished')], default='Waiting', help_text='Поставьте стстус', max_length=16, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Teacher', 'Teacher'), ('Student', 'Student')], default='Student', max_length=8, verbose_name='Роль'),
        ),
        migrations.AddConstraint(
            model_name='bunch',
            constraint=models.UniqueConstraint(fields=('teacher', 'student', 'datetime'), name='unique_bunch'),
        ),
    ]
