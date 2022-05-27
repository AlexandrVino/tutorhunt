from typing import Union

from django.db import models

from graphics.utils import DayTimeline
from graphics.formfields import DayTimelineFormField


class DayTimelineField(models.CharField):
    """Поле, обозначающее расписание в рамках одного дня"""

    description = "Поле, обозначающее расписание в рамках одного дня"
    initial = {
        "null": False,
        "help_text": "Обозначьте часы, в которые вы заняты",
        "max_length": 24
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(self.initial)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value: DayTimeline) -> str:
        return str(value)

    def from_db_value(self, value: str, expression, connection) -> str:
        return DayTimeline.parse_timeline(value)

    def to_python(self, value: Union[DayTimeline, str]) -> DayTimeline:
        if isinstance(value, DayTimeline):
            return value
        return DayTimeline.parse_timeline(value)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": DayTimelineFormField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
