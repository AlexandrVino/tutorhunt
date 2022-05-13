from django.contrib import admin
from notifications.models import NotificationModel


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    empty_value_display = "(null)"
    list_display = ("__str__", "category", "recipient", "initiator", "creation")
