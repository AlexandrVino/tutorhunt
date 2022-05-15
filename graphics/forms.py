from django.forms import ModelForm
from .models import TimelineModel

class TimelineForm(ModelForm):
    # def __init__(self, classes: Optional[Iterable[str]]=None, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)

    #     if classes:
    #         self.add_css_class_to_field(classes)

    # def add_css_class_to_field(self, classes: Iterable[str]) -> None:
    #     """
    #     Позволет добавить css класс во все поля формы

    #     Параметры:
    #     classes -- список с именами классов
    #     """
    #     str_classes = " ".join(classes)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs["class"] = str_classes

    class Meta:
        model = TimelineModel
        exclude = ("user", )
