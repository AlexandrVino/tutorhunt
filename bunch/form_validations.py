from bunch.models import Bunch, BunchStatus


def bunch_form_validation(form):
    data = form.__dict__.get("data")
    if Bunch.manager.filter(datetime=data.get("datetime"), status=BunchStatus.ACCEPTED):
        form.add_error("datetime", "Время занято")
    return form.is_bound and not form.errors
