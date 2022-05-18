# Generated by Django 3.2.13 on 2022-05-13 16:11

from django.db import migrations
import graphics.fields


class Migration(migrations.Migration):

    dependencies = [
        ('graphics', '0005_auto_20220513_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelinemodel',
            name='friday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='пятница'),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='monday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='понедельник'),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='saturday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='суббота'),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='sunday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='воскресенье'),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='thursday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='четверг'),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='tuesday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='вторник'),
        ),
        migrations.AlterField(
            model_name='timelinemodel',
            name='wednesday',
            field=graphics.fields.DayTimelineField(default=graphics.fields.DayTimeline(timeline=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)), help_text='Обозначьте часы, в которые вы заняты', max_length=24, verbose_name='среда'),
        ),
    ]
