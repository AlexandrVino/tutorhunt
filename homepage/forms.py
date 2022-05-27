from django import forms

from users.models import User


class SearchForm(forms.ModelForm):
    value = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-dark me-1",
        "type": "text",
        "placeholder": "Ключевое слово/фраза",
        "id": "value",
    }), )

    class Meta:
        model = User
        fields = ("value", )
