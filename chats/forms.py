from django import forms

from chats.models import Message


class AddMessage(forms.ModelForm):
    """
    Класс формы отправки сообщений
    """

    # role = forms.ChoiceField(choices=Role.choices)
    text = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control input-field send-mess",
        "type": "text",
        "placeholder": "Введите сообщение...",
        "id": "input_message",
        "required": True,
    }), required=True)
    # images = forms.FileField(widget=forms.FileInput(attrs={
    #     "class": "form-control input-field input-file",
    #     "placeholder": "Фото",
    #     "required": False,
    #     "type": "file"
    # }), required=False)

    class Meta:
        model = Message
        fields = ("text", )
