from django.contrib import admin
from notifications.models import NotificationModel, NotificationQueryset


@admin.action(description="Отметить прочитанными")
def mark_read(model_admin, request, queryset: NotificationQueryset):
    queryset.mark_read()


@admin.action(description="Отметить непрочитанными")
def mark_unread(model_admin, request, queryset: NotificationQueryset):
    queryset.mark_unread()


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    empty_value_display = "(null)"
    list_display = ("category", "recipient", "initiator", "creation", "read")
    list_editable = ("read", )
    actions = (mark_read, mark_unread)
