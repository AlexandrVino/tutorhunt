from django.contrib.auth import get_user_model
from django.db import models

from chats.managers import ChatRoomManager, MessagesManager

User = get_user_model()


class ChatRoom(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_user")
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second_name")

    manager = ChatRoomManager()

    def send_message(self, model, sender: User, text: str, images: list = None) -> bool:
        model.manager.create(chat_room=self, owner=sender, text=text, image=None)
        return True

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Message(models.Model):

    text = models.CharField(max_length=255)
    image = models.ImageField(blank=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default=None)

    manager = MessagesManager()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
