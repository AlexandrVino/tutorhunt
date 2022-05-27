from django import forms

from bunch.models import Bunch, BunchStatus


def bunch_form_validation(form: forms.ModelForm) -> bool:
    """
    Функция проверки формы на валидность
    Параметры:
        form: forms.ModelForm
    Возвращет bool
    """
    data = form.__dict__.get("data")
    if Bunch.manager.filter(datetime=data.get("datetime"), status=BunchStatus.ACCEPTED):
        form.add_error("datetime", "Время занято")
    return form.is_bound and not form.errors
