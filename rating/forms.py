from django import forms

from rating.models import Rating


class RatingForm(forms.Form):
    CHOICES = Rating.choices
    star = forms.ChoiceField(
        choices=CHOICES,
        label="Оценка",
        widget=forms.Select(
            attrs={"class": "form-control input-field", "id": "select_rate"}
        ),
    )

    rating_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Rating
        fields = ("star",)
