from django.contrib import admin
from notifications.models import NotificationModel


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    empty_value_display = "(null)"
    list_display = ("category", "recipient", "initiator", "creation", "read")
    list_editable = ("read", )
