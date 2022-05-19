from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView, ListView

from chats.forms import AddMessage
from chats.models import ChatRoom, Message
from chats.utils import get_interlocutor, get_interlocutor_with_id

MESSAGES_TEMPLATE = "chats/chats.html"
CHATS_TEMPLATE = "chats/all_chats.html"

User = get_user_model()


@method_decorator(login_required, name="dispatch")
class ChatsView(DetailView, FormView):
    template_name = MESSAGES_TEMPLATE
    model = ChatRoom
    context_object_name = "chat"
    current_user = None
    object = None
    form_class = AddMessage
    messages = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = self.form_class()
        context["message"] = self.messages
        context["interlocutor"] = get_interlocutor(self.object, self.current_user)
        context["chat_messages"] = Message.manager.join_owners(chat_room=self.object)

        return context

    def get_object(self, queryset=None):
        if self.object:
            return self.object

        user_id = self.kwargs.get("user_id")
        curr_user_id = self.current_user.id

        try:
            chats = self.model.manager.join_owners(id=self.kwargs.get("chat_id")) or self.model.manager.join_owners(
                first_user_id__in=(user_id, curr_user_id), second_user_id__in=(curr_user_id, user_id))
            chat = chats and chats[0]

            assert chat
            return chat

        except AssertionError:
            return (self.model.manager.create(first_user=self.current_user, second_user_id=self.kwargs.get("user_id"))
                    if self.kwargs.get("user_id") else None)

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        self.object = self.get_object()

        if self.current_user.id not in (self.object.first_user.id, self.object.second_user.id):
            return redirect(reverse("user_detail", args=(self.current_user.id,)))

        return super(ChatsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():

            if not self.current_user:
                self.current_user = request.user

            self.object = self.get_object()
            self.object.send_message(Message, self.current_user, form.cleaned_data["text"])
            form.clean()

        else:
            self.messages.extend([err["text"] if type(err) is dict else err for err in form.errors])

        return super(ChatsView, self).get(request, *args, **kwargs)


class ChatsListView(ListView):
    """Возвращает страничку Списка пользователей"""

    template_name = CHATS_TEMPLATE
    context_object_name = "chats"

    def get_queryset(self):
        user = self.request.user

        return set(chain(
            map(lambda x: (x, get_interlocutor_with_id(x, user.id)),
                ChatRoom.manager.join_owners(first_user_id=user.id)),
            map(lambda x: (x, get_interlocutor_with_id(x, user.id)),
                ChatRoom.manager.join_owners(second_user_id=user.id))
        ))
