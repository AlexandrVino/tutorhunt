from django import forms
from bunch.models import Bunch, BunchStatus
from graphics.utils import CONST as TIMELINE_CONST


class AddBunchForm(forms.ModelForm):
    """Форма для планирования (создания) связи (занятия)"""
    day = forms.ChoiceField(choices=TIMELINE_CONST.WEEKDAYS_RUS_CHOICES)

    time = forms.ChoiceField(choices=TIMELINE_CONST.HOURS_CHOICES)

    user_from = forms.IntegerField(widget=forms.FileInput(attrs={
        "class": "form-control input-field input-file",
        "placeholder": "Id пользователя",
        "required": False,
        "type": "text"
    }), required=False)

    user_to = forms.IntegerField(widget=forms.FileInput(attrs={
        "class": "form-control input-field input-file",
        "placeholder": "Id пользователя",
        "required": False,
        "type": "text"
    }), required=False)

    class Meta:
        model = Bunch
        fields = ("user_from", "user_to", "day", "time")


class EditBunchForm(forms.ModelForm):
    """Форма, чтобы учитель мог подтвердить/отредактировать связь (занятие)"""
    status = forms.ChoiceField(choices=BunchStatus.choices)

    day = forms.ChoiceField(choices=TIMELINE_CONST.WEEKDAYS_RUS_CHOICES)

    time = forms.ChoiceField(choices=TIMELINE_CONST.HOURS_CHOICES)

    user_to = forms.IntegerField(widget=forms.FileInput(attrs={
        "class": "form-control input-field input-file",
        "placeholder": "Id пользователя",
        "required": False,
        "type": "text"
    }), required=False)

    class Meta:
        model = Bunch
        fields = ("user_to", "day", "time")
