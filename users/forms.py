from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Bunch, BunchStatus, Follow, Role, User


class LoginForm(forms.ModelForm):
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

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "role",
            "first_name",
            "last_name",
            "photo",
        )


class EditProfileForm(forms.ModelForm):
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

    class Meta:
        model = User
        fields = ("first_name", "last_name", "photo")


class FollowForm(forms.ModelForm):
    follow = forms.BooleanField()

    class Meta:
        model = Follow
        fields = ("follow",)


class AddBunchForm(forms.ModelForm):
    day = forms.ChoiceField(
        choices=(
            (1, "Понедельник"),
            (2, "Вторник"),
            (3, "Среда"),
            (4, "Четверг"),
            (5, "Пятница"),
            (6, "Суббота"),
            (7, "Воскресенье"),
        )
    )
    time = forms.ChoiceField(choices=((i, "%02d:00" % i) for i in range(24)))
    user_from = forms.IntegerField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control input-field input-file",
                "placeholder": "Id пользователя",
                "required": False,
                "type": "text",
            }
        ),
        required=False,
    )

    user_to = forms.IntegerField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control input-field input-file",
                "placeholder": "Id пользователя",
                "required": False,
                "type": "text",
            }
        ),
        required=False,
    )

    class Meta:
        model = Bunch
        fields = ("user_from", "user_to", "day", "time")


class EditBunchForm(forms.ModelForm):
    status = forms.ChoiceField(choices=BunchStatus.choices)
    day = forms.ChoiceField(
        choices=(
            (1, "Понедельник"),
            (2, "Вторник"),
            (3, "Среда"),
            (4, "Четверг"),
            (5, "Пятница"),
            (6, "Суббота"),
            (7, "Воскресенье"),
        )
    )
    time = forms.ChoiceField(choices=((i, "%02d:00" % i) for i in range(24)))

    user_to = forms.IntegerField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control input-field input-file",
                "placeholder": "Id пользователя",
                "required": False,
                "type": "text",
            }
        ),
        required=False,
    )

    class Meta:
        model = Bunch
        fields = ("user_to", "day", "time")
