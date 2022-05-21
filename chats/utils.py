from django.contrib.auth import get_user_model

from chats.models import ChatRoom

User = get_user_model()


def get_interlocutor_with_id(chat: ChatRoom, user_id: int) -> User:
    """

   :param chat: ChatRoom текущая комната
   :param user_id: int id текущего юзера
   :return: User

   Метод возвращения собеседника по id

   """

    return chat.first_user if chat.first_user.id != user_id else chat.second_user
