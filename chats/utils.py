from django.contrib.auth import get_user_model

from chats.models import ChatRoom

User = get_user_model()


def get_interlocutor(chat: ChatRoom, user: User) -> User:
    return chat.first_user if chat.first_user.id != user.id else chat.second_user


def get_interlocutor_with_id(chat: ChatRoom, user_id: int) -> User:
    return chat.first_user if chat.first_user.id != user_id else chat.second_user


