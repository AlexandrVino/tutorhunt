from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Role, User


class SearchForm(forms.ModelForm):
    value = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={
        "class": "form-control me-1",
        "type": "text",
        "placeholder": "Ключивое слово/фраза",
        "id": "value",
    }), )

    class Meta:
        model = User
        fields = ("value", )
