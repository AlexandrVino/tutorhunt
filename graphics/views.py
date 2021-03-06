from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from graphics.utils import CONST

from .utils import DayTimeline
from .forms import TimelineForm
from .models import TimelineModel

TIMELINE_VIEW_TEMPLATE = "graphics/view_timeline.html"
EDIT_TIMELINE_TEMPLATE = "graphics/edit_template.html"


class TimelineView(DetailView):
    template_name = TIMELINE_VIEW_TEMPLATE
    model = TimelineModel
    object = None

    def get_object(self, queryset=None):
        if self.object:
            return self.object
        return super(TimelineView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        object: TimelineModel = self.get_object()
        table_data = object.get_table_data()

        context = super().get_context_data(**kwargs)
        context["headers"] = table_data["headers"]
        context["table_data"] = table_data["data"]
        return context


@method_decorator(login_required, name="dispatch")
class EditTimelineView(UpdateView):
    template_name = EDIT_TIMELINE_TEMPLATE
    model = TimelineModel
    form_class = TimelineForm

    def get_success_url(self) -> str:
        return self.get_object().user.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.id == self.get_object().user.id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_initial(self) -> Dict[str, Any]:
        initial = dict()
        timeline: TimelineModel = self.get_object()

        for weekday in CONST.WEEKDAYS:
            weekday_timeline: DayTimeline = timeline.__dict__[weekday]
            initial[weekday] = weekday_timeline.get_form_initial()
        return initial

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["label_suffix"] = ""
        return kwargs

    def get_object(self, *args, **kwargs) -> TimelineModel:
        self.kwargs.setdefault("pk", self.request.user.timeline.pk)
        return TimelineModel.objects.get(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
