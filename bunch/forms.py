from django import forms
from bunch.models import Bunch, BunchStatus


class AddBunchForm(forms.ModelForm):

    """
    Форма для планирования (создания) связи (занятия)
    """

    day = forms.ChoiceField(choices=(
        (1, "Понедельник"),
        (2, "Вторник"),
        (3, "Среда"),
        (4, "Четверг"),
        (5, "Пятница"),
        (6, "Суббота"),
        (7, "Воскресенье"),
    ))

    time = forms.ChoiceField(choices=((i, "%02d:00" % i) for i in range(24)))

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

    """
    Форма, чтобы учитель мог подтвердить/отредактировать связь (занятие)
    """

    status = forms.ChoiceField(choices=BunchStatus.choices)

    day = forms.ChoiceField(choices=(
        (1, "Понедельник"),
        (2, "Вторник"),
        (3, "Среда"),
        (4, "Четверг"),
        (5, "Пятница"),
        (6, "Суббота"),
        (7, "Воскресенье"),
    ))

    time = forms.ChoiceField(choices=((i, "%02d:00" % i) for i in range(24)))

    user_to = forms.IntegerField(widget=forms.FileInput(attrs={
        "class": "form-control input-field input-file",
        "placeholder": "Id пользователя",
        "required": False,
        "type": "text"
    }), required=False)

    class Meta:
        model = Bunch
        fields = ("user_to", "day", "time")
