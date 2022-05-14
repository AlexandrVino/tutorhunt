from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name="dispatch")
class NotificationListView(View):
    pass