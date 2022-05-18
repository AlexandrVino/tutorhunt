from django.forms import ModelForm
from .models import TimelineModel

class TimelineForm(ModelForm):
    class Meta:
        model = TimelineModel
        exclude = ("user", )
