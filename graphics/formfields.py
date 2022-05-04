from typing import List
from django.forms import CheckboxSelectMultiple, MultipleChoiceField


class DayTimelineFormField(MultipleChoiceField):
    """Поле для выбора расписания в форме"""
    from graphics.fields import DayTimeline
    
    _choices = [(i, i) for i in range(1, 25)]

    def __init__(self, *args, **kwargs):
        if "max_length" in kwargs:
            del kwargs["max_length"]

        if "initial" in kwargs:
            kwargs["initial"] = kwargs["initial"].get_form_initial()

        kwargs["widget"] = CheckboxSelectMultiple
        kwargs["choices"] = self._choices

        super().__init__(*args, **kwargs)

    def clean(self, value: List[str]) -> DayTimeline:
        return self.DayTimeline.parse_formfield(value)