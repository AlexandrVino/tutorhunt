from django.urls import path
from follow.views import FollowersListView

urlpatterns = [
    path("<int:user_to>/", FollowersListView.as_view(), name="user_detail_follows"),
]
