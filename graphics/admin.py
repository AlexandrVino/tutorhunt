from django.contrib import admin
from .models import TimelineModel


@admin.register(TimelineModel)
class TimelineAdmin(admin.ModelAdmin):
    pass
