from django import forms

from follow.models import Follow


class FollowForm(forms.ModelForm):
    """
    Класс формы подписки
    """

    follow = forms.BooleanField()

    class Meta:
        model = Follow
        fields = ("follow",)
