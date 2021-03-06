from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from chats.managers import ChatRoomManager, MessagesManager

User = get_user_model()


class ChatRoom(models.Model):
    """Класс модели комнаты чата"""
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="first_user")
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="second_user")

    manager = ChatRoomManager()

    def send_message(self, model, sender: User, text: str, images: list = None):
        model.manager.create(
            chat_room=self,
            owner=sender,
            text=text,
            image=None,
            time=datetime.now().time()
        )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class Message(models.Model):
    """Класс модели сообщения"""
    text = models.TextField()
    image = models.ImageField(blank=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    time = models.TimeField(verbose_name="Время отправки", null=True)

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default=None)

    manager = MessagesManager()

    def get_recipient(self) -> User:
        """Возвращает получателя сообщения (для грязных целей обработчика уведомлений)"""
        first_user, second_user = self.chat_room.first_user, self.chat_room.second_user
        if not first_user == self.owner:
            return first_user
        return second_user

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
