from django.urls import path
from chats.views import ChatsView

urlpatterns = [
    path("<int:user_to>/", ChatsView.as_view()),
]
