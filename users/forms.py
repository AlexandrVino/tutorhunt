from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Role, User


class LoginForm(forms.ModelForm):
    """Форма входа"""
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Почта",
                "required": False,
                "type": "email",
            }
        )
    )

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control input-field",
                "type": "password",
                "placeholder": "Пароль",
                "id": "password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password")


class RegisterForm(UserCreationForm):
    """Форма регистрации"""
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "type": "text",
                "placeholder": "Никнейм",
                "id": "username",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Почта",
                "required": True,
                "type": "email",
            }
        )
    )
    password1 = forms.CharField(
        strip=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Придумайте пароль",
                "type": "password",
            }
        ),
    )
    password2 = forms.CharField(
        strip=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Повторите пароль",
                "type": "password",
            }
        ),
    )
    role = forms.ChoiceField(choices=Role.choices)

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "type": "text",
                "placeholder": "Имя",
                "id": "first_name",
                "required": False,
            }
        ),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "type": "text",
                "placeholder": "Фамилия",
                "id": "last_name",
                "required": False,
            }
        ),
        required=False,
    )
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control input-field input-file",
                "placeholder": "Фото",
                "required": False,
                "type": "file",
            }
        ),
        required=False,
    )

    bio = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control input-field",
        "type": "text",
        "placeholder": "Расскажите о себе",
        "id": "bio",
        "required": False,
    }), required=False)

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2",
            "role", "first_name", "last_name", "photo", "bio"
        )


class EditProfileForm(forms.ModelForm):
    """Форма редактироваия профиля"""
    # role = forms.ChoiceField(choices=Role.choices)

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "type": "text",
                "placeholder": "Имя",
                "id": "first_name",
                "required": False,
            }
        ),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "type": "text",
                "placeholder": "Фамилия",
                "id": "last_name",
                "required": False,
            }
        ),
        required=False,
    )
    photo = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control input-field input-file",
                "placeholder": "Фото",
                "required": False,
                "type": "file",
            }
        ),
        required=False,
    )
    bio = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control input-field",
        "type": "text",
        "placeholder": "Расскажите о себе",
        "id": "bio",
        "required": False,
    }), required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "photo", "bio")
