# Generated by Django 3.2.13 on 2022-05-03 18:02

from django.db import migrations, models
import graphics.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimelineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='понедельник')),
                ('tuesday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='вторник')),
                ('wednesday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='среда')),
                ('thursday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='четверг')),
                ('friday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='пятница')),
                ('saturday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='суббота')),
                ('sunday', graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='воскресенье')),
            ],
            options={
                'verbose_name': 'расписание',
                'verbose_name_plural': 'расписания',
            },
        ),
    ]
