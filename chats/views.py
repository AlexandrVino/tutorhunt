from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, FormView

from chats.forms import AddMessage
from chats.models import ChatRoom, Message

MESSAGES_TEMPLATE = "chats/chats.html"
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
        context["message"] = self.messages
        context["chat_messages"] = Message.manager.join_owners(chat_room=self.object)
        context["form"] = self.form_class()
        return context

    def get_object(self, queryset=None):
        if self.object:
            return self.object
        try:
            chats = (
                    self.model.manager.filter(
                        first_user_id=self.current_user.id, second_user=self.kwargs.get("user_to")) or
                    self.model.manager.filter(
                        second_user=self.current_user.id, first_user_id=self.kwargs.get("user_to"))
            )
            chat = chats and chats[0]

            assert chat
            return chat

        except AssertionError:
            user_to = User.manager.filter(id=self.kwargs.get("user_to"))
            if not user_to:
                return None
            return self.model.manager.create(first_user=self.current_user, second_user=user_to[0])

    def get(self, request, *args, **kwargs):
        self.current_user = request.user
        if not self.object:
            self.object = self.get_object()

        if self.current_user.id not in (self.object.first_user.id, self.object.second_user.id):
            return redirect(reverse("user_detail", args=(self.current_user.id,)))

        return super(ChatsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            if not self.current_user:
                self.current_user = request.user

            if not self.object:
                self.object = self.get_object()
            self.object.send_message(Message, self.current_user, form.cleaned_data["text"])
            form.clean()

        else:
            self.messages.extend([err["text"] if type(err) is dict else err for err in form.errors])

        return super(ChatsView, self).get(request, *args, **kwargs)
