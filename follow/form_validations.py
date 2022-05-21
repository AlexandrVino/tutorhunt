def follow_form_validation(form):
    data = form.__dict__.get("data")
    if data.get("user_from") == data.get("user_to"):
        form.add_error("user_to", "Пользователь не может быть подписан сам на себя")
    return form.is_bound and not form.errors
