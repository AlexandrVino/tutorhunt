from django.urls import path
from notifications.views import NotificationListView

urlpatterns = [
    path("page/<int:page>/", NotificationListView.as_view(), name="page-notifications"),
    path("", NotificationListView.as_view(), name="notifications")
]
