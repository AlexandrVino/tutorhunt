from django.urls import path
from .views import TimelineView, EditTimelineView

urlpatterns = [
    path("view/<int:pk>", TimelineView.as_view(), name="detail-timeline"),
    path("edit/<int:pk>", EditTimelineView.as_view(), name="edit-timeline")
]
