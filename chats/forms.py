from django import forms

from chats.models import Message


class AddMessage(forms.ModelForm):
    """Класс формы отправки сообщений"""
    text = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control input-field send-mess",
        "type": "text",
        "placeholder": "Введите сообщение...",
        "id": "input_message",
        "required": True,
    }), required=True)

    class Meta:
        model = Message
        fields = ("text", )
