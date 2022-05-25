from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from follow.models import Follow

USER_LIST_TEMPLATE = "users/user_list.html"

User = get_user_model()


@method_decorator(login_required, name="dispatch")
class FollowersListView(DetailView):
    """Возвращает страничку Списка подписок пользователя"""

    template_name = USER_LIST_TEMPLATE
    model = User
    pk_url_kwarg = "user_to"

    current_user = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = map(
            lambda x: x.user_from,
            Follow.manager.get_followers(
                None, "user_from__first_name", "user_from__photo",
                "user_from__last_name", "user_from__username",
                "user_from__email", "user_from__role",
                user_to=self.object))
        return context
