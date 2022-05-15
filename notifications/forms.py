from django.forms import (ChoiceField, ModelChoiceField,
                          ModelForm, Select)

from notifications.models import CATEGORY_CHOICES, NotificationModel
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminFilterNotificationsForm(ModelForm):
    category = ChoiceField(
        choices=CATEGORY_CHOICES + ((None, "--------"), ),
        widget=Select(attrs={"class": "form-control"}),
        required=False
    )
    recipient = ModelChoiceField(queryset=User.objects.all(), widget=Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = NotificationModel
        fields = ("category", "recipient")


class FilterNotificationsForm(ModelForm):
    category = ChoiceField(choices=CATEGORY_CHOICES, widget=Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = NotificationModel
        fields = ("category", )
