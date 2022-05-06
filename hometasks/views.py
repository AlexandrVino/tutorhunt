from typing import Any, Dict
from django.forms import BoundField

from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from .fields import DayTimeline
from .forms import TimelineForm
from .models import TimelineModel


TIMELINE_VIEW_TEMPLATE = "graphics/view_timeline.html"
EDIT_TIMELINTE_TEMPLATE = "graphics/edit_template.html"

WEEKDAYS = ("monday", "tuesday",
            "wednesday", "thursday",
            "friday", "saturday", "sunday")


class TimelineView(DetailView):
    template_name = TIMELINE_VIEW_TEMPLATE
    model = TimelineModel

class EditTimelineView(UpdateView):
    template_name = EDIT_TIMELINTE_TEMPLATE
    model = TimelineModel
    form_class = TimelineForm
    css_classes = ("visually-hidden", )

    def get(self, *args, **kwargs):
        # for f in self.get_form():
        #     print(f.field.widget.__dict__)

        # for f in self.get_form().fields.values():
        #     print(f.__class__)

        return super().get(*args, **kwargs)

    def get_initial(self) -> Dict[str, Any]:
        initial = dict()
        timeline: TimelineModel = self.get_object()

        for weekday in WEEKDAYS:
            weekday_timeline: DayTimeline = timeline.__dict__[weekday]
            initial[weekday] = weekday_timeline.get_form_initial()
        return initial
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["label_suffix"] = ""
        # kwargs["classes"] = self.css_classes
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["options"] = self.get
        return context
    
