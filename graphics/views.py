from typing import Any, Dict
from django.http import HttpResponseForbidden

from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .fields import DayTimeline
from .forms import TimelineForm
from .models import WEEKDAYS_RUS, TimelineModel


TIMELINE_VIEW_TEMPLATE = "graphics/view_timeline.html"
EDIT_TIMELINTE_TEMPLATE = "graphics/edit_template.html"

WEEKDAYS = ("monday", "tuesday",
            "wednesday", "thursday",
            "friday", "saturday", "sunday")
HOURS = tuple(['%02d:00' % i for i in range(24)])


class TimelineView(DetailView):
    template_name = TIMELINE_VIEW_TEMPLATE
    model = TimelineModel

    def get_context_data(self, **kwargs):
        object: TimelineModel = self.get_object()

        table_data = [[None for __ in range(7)] for _ in range(24)]

        for i, weekday in enumerate(object.get_days_fields()):
            for j in range(24):
                table_data[j][i] = {
                    "value": HOURS[j],
                    "class": "busy-hour" if weekday.is_busy(j) else "vacant-hour"
                    }

        context = super().get_context_data(**kwargs)
        context["headers"] = WEEKDAYS_RUS
        context["table_data"] = table_data
        return context


@method_decorator(login_required, name='dispatch')
class EditTimelineView(UpdateView):
    template_name = EDIT_TIMELINTE_TEMPLATE
    model = TimelineModel
    form_class = TimelineForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.id == self.get_object().user.id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()


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
