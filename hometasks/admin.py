from django.contrib import admin
from .models import TimelineModel


@admin.register(TimelineModel)
class TimlineAdmin(admin.ModelAdmin):
    pass
