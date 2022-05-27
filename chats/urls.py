from django.urls import path
from chats.views import ChatsView, ChatsListView

urlpatterns = [
    path("<int:chat_id>/<int:user_id>/", ChatsView.as_view(), name="current_chat"),
    path("", ChatsListView.as_view(), name="all_chats"),
]
