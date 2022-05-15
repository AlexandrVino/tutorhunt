from users.models import Bunch, BunchStatus


def follow_form_validation(form):
    data = form.__dict__.get('data')
    if data.get('user_from') == data.get('user_to'):
        form.add_error('user_to', 'Пользователь не может быть подписан сам на себя')
    return form.is_bound and not form.errors


def bunch_form_validation(form):
    data = form.__dict__.get('data')
    if Bunch.manager.filter(datetime=data.get('datetime'), status=BunchStatus.ACCEPTED):
        form.add_error('datetime', 'Время занято')
    return form.is_bound and not form.errors
