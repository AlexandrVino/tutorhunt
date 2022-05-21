from django import forms

from .models import Assignment, Hometask


class HometaskForm(forms.ModelForm):
    title = forms.CharField(
        strip=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Название",
                "type": "text",
            }
        ),
    )
    description = forms.CharField(
        strip=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Описание",
                "type": "text",
            }
        ),
    )
    files = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control input-field input-file",
                "placeholder": "Файл",
                "type": "file",
            }
        ),
        required=False,
    )

    class Meta:
        model = Hometask
        fields = ("title", "description", "files")


class AssignmentForm(forms.ModelForm):
    student = forms.CharField(
        strip=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Название",
                "type": "text",
            }
        ),
    )
    hometask = forms.CharField(
        strip=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control input-field",
                "placeholder": "Описание",
                "type": "text",
            }
        ),
    )

    class Meta:
        model = Assignment
        fields = ("hometask", "student")


class IsCompletedForm(forms.ModelForm):
    is_completed = forms.BooleanField()

    class Meta:
        model = Assignment
        fields = ("is_completed",)
